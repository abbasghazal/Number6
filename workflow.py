"""Persistent progress and cooperative cancellation at safe work boundaries."""
import asyncio
import contextvars
import functools
import inspect
import secrets

enabled = False
current_job = contextvars.ContextVar('current_job', default=None)


async def query(*args, **kwargs):
    from helpers import execute_query
    return await execute_query(*args, **kwargs)


class JobStopped(asyncio.CancelledError):
    pass


async def initialize():
    global enabled
    await query("UPDATE workflow_jobs SET status='interrupted', message='انقطع التشغيل؛ لم تُستأنف هذه المحاولة', updated_at=CURRENT_TIMESTAMP WHERE status='running'", commit=True)
    rows = await query("""SELECT j.job_id,j.user_id,COUNT(r.phone) FROM workflow_jobs j
        LEFT JOIN search_join_results r ON r.job_id=j.job_id WHERE j.kind='search_join' AND j.status='interrupted'
        GROUP BY j.job_id,j.user_id""",fetchall=True) or []
    for job,user,count in rows:
        await queue_notice(user,f'search:interrupted:{job}',
                           f'انقطعت مهمة البحث {job}. النتائج المحفوظة: {count}. النتائج غير المحسومة لا تُعاد تلقائيًا؛ راجع مركز المهام.')
    await query("UPDATE backup_runs SET restore_status='interrupted' WHERE restore_status='running'", commit=True)
    await query("UPDATE backup_runs SET status='interrupted' WHERE status='running'", commit=True)
    from recurring_jobs import recover
    await recover()
    enabled = True


async def progress(*, total=None, processed=None, success=None, failed=None, message=None):
    job = current_job.get()
    if not job:
        return
    row = await query('''UPDATE workflow_jobs SET
        total=COALESCE(?,total), processed=COALESCE(?,processed),
        success=COALESCE(?,success), failed=COALESCE(?,failed),
        message=COALESCE(?,message), updated_at=CURRENT_TIMESTAMP
        WHERE job_id=? RETURNING cancel_requested''',
        (total, processed, success, failed, message, job), commit=True, fetchone=True)
    if row and row[0]:
        raise JobStopped()


async def note_failure(message):
    if current_job.get():
        await query("UPDATE workflow_jobs SET status='failed', message=?, updated_at=CURRENT_TIMESTAMP WHERE job_id=?",
                    (message[:300], current_job.get()), commit=True)


def tracked(kind, owner='user_id', *, event=False, cancellable=True):
    def decorate(fn):
        signature = inspect.signature(fn)

        @functools.wraps(fn)
        async def wrapped(*args, **kwargs):
            if not enabled or current_job.get():
                return await fn(*args, **kwargs)
            values = signature.bind(*args, **kwargs).arguments
            user = values[owner]
            if event:
                user = user.chat_id
            job = secrets.token_hex(8)
            await query('''INSERT INTO workflow_jobs(job_id,user_id,kind,cancellable)
                           VALUES(?,?,?,?)''', (job, user, kind, cancellable), commit=True)
            token = current_job.set(job)
            state, message = 'completed', None
            try:
                return await fn(*args, **kwargs)
            except JobStopped:
                state, message = 'cancelled', 'أُلغي الطلب؛ النتائج المكتملة محفوظة'
            except asyncio.CancelledError:
                state, message = 'interrupted', 'توقفت المهمة أثناء الإغلاق أو بأمر إيقاف الخدمة'
                raise
            except Exception:
                state, message = 'failed', 'تعذر إكمال المهمة؛ راجع نتائج الخدمة'
                raise
            finally:
                current_job.reset(token)
                await query('''UPDATE workflow_jobs SET status=?, message=COALESCE(?,message),
                    updated_at=CURRENT_TIMESTAMP WHERE job_id=? AND status='running' ''',
                    (state, message, job), commit=True)
        return wrapped
    return decorate


async def pause(seconds):
    """Long service sleeps remain interruptible through the job center."""
    loop = asyncio.get_running_loop()
    end = loop.time() + max(0, seconds)
    while loop.time() < end:
        await asyncio.sleep(min(5, end - loop.time()))
        await progress()


def enqueue(db, user_id, key, message):
    db.execute('''INSERT INTO operation_notices(user_id,dedupe_key,message)
                  VALUES(?,?,?) ON CONFLICT(dedupe_key) DO NOTHING''', (user_id, key, message))


async def queue_notice(user_id, key, message):
    await query('''INSERT INTO operation_notices(user_id,dedupe_key,message)
                   VALUES(?,?,?) ON CONFLICT(dedupe_key) DO NOTHING''',
                (user_id, key, message), commit=True)


async def deliver_notices(client):
    from telethon.errors import FloodWaitError
    rows = await query('''SELECT notice_id,user_id,message,dedupe_key FROM operation_notices
        WHERE sent_at IS NULL AND next_attempt<=CURRENT_TIMESTAMP
        AND NOT EXISTS(SELECT 1 FROM platform_preferences p WHERE p.user_id=operation_notices.user_id AND NOT p.notifications)
        ORDER BY notice_id LIMIT 30''', fetchall=True)
    for notice_id, user_id, message, key in rows or []:
        from service_health import tick
        tick('platform')
        buttons = None
        if key.startswith(('ticket:staff:', 'ticket:reply:')):
            from support_center import detail
            ticket_id = int(key.split(':')[2]) if key.startswith('ticket:staff:') else None
            if ticket_id is None:
                row = await query('SELECT ticket_id FROM ticket_messages WHERE message_id=?', (int(key.split(':')[2]),), fetchone=True)
                ticket_id = row[0] if row else None
            try:
                if ticket_id is None:
                    raise ValueError('missing ticket')
                await detail(user_id, ticket_id)
            except ValueError:
                await query('UPDATE operation_notices SET sent_at=CURRENT_TIMESTAMP WHERE notice_id=?', (notice_id,), commit=True)
                continue
            from keyboards import Button
            buttons = [[Button.inline('فتح التذكرة والرد', data=f'feature:tickets:view:{ticket_id}')]]
        if key.startswith('ticket:message:'):
            message_id = int(key.rsplit(':', 1)[1])
            destination = await query('''SELECT t.user_id,t.assigned_to,m.is_staff
                FROM ticket_messages m JOIN support_tickets t ON t.ticket_id=m.ticket_id WHERE m.message_id=?''',
                (message_id,), fetchone=True)
            if not destination:
                await query('UPDATE operation_notices SET sent_at=CURRENT_TIMESTAMP WHERE notice_id=?', (notice_id,), commit=True)
                continue
            from config import ADMIN_ID
            from staff_security import has_permission
            owner, assigned, is_staff_message = destination
            recipient = owner if is_staff_message else assigned if assigned and await has_permission(assigned, 'support') else ADMIN_ID
            if recipient != user_id:
                await query('UPDATE operation_notices SET user_id=? WHERE notice_id=?', (recipient, notice_id), commit=True)
                user_id = recipient
        if key.startswith('watch:'):
            parts = key.split(':')
            watch = await query('''SELECT stock_alert,price_alert FROM country_watches
                WHERE user_id=? AND country_id=? AND service=?''',
                (user_id, int(parts[2]), parts[3]), fetchone=True)
            from helpers import is_banned
            subscribed = bool(watch and (watch[0] if parts[-1] == 'stock' else watch[1] if parts[-1] == 'price' else any(watch)))
            if not subscribed or await is_banned(user_id):
                await query('UPDATE operation_notices SET sent_at=CURRENT_TIMESTAMP WHERE notice_id=?',
                            (notice_id,), commit=True)
                continue
        if key.startswith('twofa:'):
            phone = key.split(':')[1]
            owners = await query('''SELECT user_id FROM stored_accounts WHERE phone=?
                UNION SELECT user_id FROM purchased_accounts WHERE phone=?''', (phone,phone), fetchall=True)
            if owners and user_id not in {r[0] for r in owners}:
                await query('UPDATE operation_notices SET sent_at=CURRENT_TIMESTAMP WHERE notice_id=?', (notice_id,), commit=True)
                continue
        try:
            await asyncio.wait_for(client.send_message(user_id, message, parse_mode=None, buttons=buttons), 20)
        except FloodWaitError as exc:
            await query("UPDATE operation_notices SET next_attempt=CURRENT_TIMESTAMP + (? * INTERVAL '1 second') WHERE sent_at IS NULL",
                        (int(exc.seconds) + 5,), commit=True)
            break
        except Exception:
            await query("UPDATE operation_notices SET next_attempt=CURRENT_TIMESTAMP + INTERVAL '1 hour' WHERE notice_id=?", (notice_id,), commit=True)
        else:
            await query('UPDATE operation_notices SET sent_at=CURRENT_TIMESTAMP WHERE notice_id=?', (notice_id,), commit=True)
            await asyncio.sleep(.25)
