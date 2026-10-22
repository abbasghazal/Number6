# Number Next Generation

أضيف **قسم API مدفوع** باشتراكات شهرية وسنوية ومفاتيح API مشفرة، مع إمكانية تشغيل خدمات البوت من Backend خارجي أو بوت آخر عبر طبقة الخدمات والـConsole API. راجع [دليل API](API_GUIDE.md).

إصلاح عزل هوية الموقع عند التحديث وتغيير الحساب، والتصفح كزائر، والكوبونات
المنتهية: [تفاصيل الإصلاح وتسجيل الدخول بعد التحديث](docs/WEB_IDENTITY_AND_COUPONS.md).

لوحة الويب في `/app` تدعم الدخول من المتصفح وTelegram Mini App، وخدمات التمويل والرشق والحسابات والمحفظة ومساحة عمل أدوات البوت. راجع [تقرير التنفيذ والإعداد](docs/NEXT_GENERATION_DELIVERY.md) و[جدول وظائف المشروع](docs/FEATURE_PARITY.md).

آخر تعديل: مكافآت اشتراك فورية، متابعة المغادرة بخصم مضاعف، فهرس جميع خدمات
البوت في الموقع، وأداة حذف المهام المنتهية. التفاصيل في [تحديث 21 أكتوبر](docs/OCTOBER_21_UPDATES.md).

كذلك يُنظف تسجيل الحساب المنصّب تلقائيًا عند تأكيد انتهاء جلسته، للسماح
بإضافته مجددًا بجلسة صالحة. [تفاصيل التنظيف](docs/SESSION_LIFECYCLE.md).

إصلاح عرض الحسابات المضافة للبيع، وفصل صلاحيات الرشق المدفوع عن التمويل:
[السبب والإصلاح](docs/INVENTORY_AND_PAID_PROMOTIONS_FIX.md).

أسعار الأرقام بالدولار حسب النوع، عند شراء المستخدم من البوت وبيعه له:
[جدول الأسعار وتطبيقه](docs/NUMBER_TYPE_PRICES.md).

# Number Store Bot deployment

تفاصيل الأنواع والأسعار والصلاحيات والأتمتة وخطوات الترحيل: [دليل تحديث أكتوبر 2026](NUMBER_TYPES_AUTOMATION.md).

بوت Telegram لإدارة وبيع وتأجير الأرقام، مع الدفع بالنجوم، المتجر، الدعم،
وإدارة الحسابات المملوكة والإيجارات السارية.

تفاصيل الرشق المدفوع والتمويل بالنقاط ومراقبة أكواد المطور وإعدادها:
[دليل الرشق والتمويل](PROMOTIONS.md).

لرفع المشروع إلى GitHub استخدم [دليل الرفع](GITHUB_UPLOAD.md). يتضمن طريقة
إنشاء نسخة نظيفة من آخر الملفات، دون الأسرار والجلسات وقاعدة البيانات المحلية.

## Local quick start

Requires Python 3.11+ and PostgreSQL. From the project directory on Windows:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
```

Use the copy command for a new installation only. Fill in the required values in
your private `.env`, then start:

```powershell
.venv\Scripts\python.exe main.py
```

For an existing installation, preserve its `.env` and `SESSION_ENCRYPTION_KEY`.
Database tables and migrations are applied automatically at startup.
`pg_dump` is required for PostgreSQL backups. On Linux, use `python3` and the
virtual environment's `.venv/bin/python`, or follow the deployment guides below.

## شهم: التجميع والتحويل والهدية

افتح **شهم · التجميع والتحويل** من القائمة الرئيسية أو قسم التحكم، أو أرسل
`/shahm` في محادثة البوت الخاصة. اختر العملية والحساب المملوك لك والبوت، ثم
راجع المعاينة وأكّد التشغيل. يستخدم القسم جلسات المشروع المحفوظة وإعداداته
الحالية، وتظهر النتائج في المحادثة والمهام في **مركز المهام**.

يدعم القسم بوتات المليار والجوكر والعقاب والعرب وبرليون واسيا وهايبر والسلطان
ودعمكم، وإدخال معرف بوت مخصص. تتوفر دورة تجميع واحدة أو دورات متكررة بفاصل
60 ثانية على الأقل، وحد من 1 إلى 100 مهمة لكل حساب في الدورة. يمكن اختيار
حسابات متعددة للتجميع والهدية، وحساب واحد للتحويل أو عرض الأزرار أو ضغط زر.

استخدم **عرض الأزرار** لمعرفة ترتيبها بدءًا من الصفر، ثم عدّل تسلسل التجميع
عند الحاجة. قد تتغير قوائم البوتات الخارجية؛ الأسماء والتسلسلات المرفقة لا
تضمن استمرار واجهاتها. تحويل دعمكم يتطلب قيمتين بالترتيب وفق تعليماته، وبقية
البوتات قيمة واحدة؛ زر تحويل هايبر غير محدد في التعريف. تُعرض استجابة البوت
كما وردت؛ لا يُعتبر إرسال الطلب تأكيدًا للتحويل أو استلام الهدية. لا يرتبط
رصيد هذه البوتات بمحفظة المشروع.

زر **إيقاف مهامي في شهم** متاح أيضًا عند انتهاء الاشتراك. تُحفظ فترات انتظار
Telegram وتُحرّر جلسة الحساب بين الدورات. عند انقطاع تشغيل المشروع تظهر
المهمة متوقفة في مركز المهام؛ ابدأها مجددًا عند الحاجة بعد مراجعة آخر نتيجة
داخل البوت المستهدف، خصوصًا للتحويل والهدية.

عند ظهور قائمة اشتراك إجباري، ينضم شهم إلى القنوات المطلوبة دون تكرار، ثم
ينفذ التحقق ويعيد فتح العملية تلقائيًا. يدعم زر التحقق العادي ورابط التحقق
الذي يعيد إلى البوت نفسه. يتوقف عند انتظار موافقة قناة خاصة أو طلب Telegram
الانتظار، ويحد محاولات التحقق بثلاث. إذا ظهرت القائمة بعد إرسال بيانات تحويل،
يعالج الاشتراك ويطلب مراجعة حالة التحويل قبل إعادة إرسال البيانات.

## Validation

```powershell
python -m pip install -r requirements-dev.txt
python -m pytest -q
npm ci
npm run test:ui
```

Node.js is used for Mini App tests; normal bot startup does not need Node.js.
Integration tests require isolated test databases, as described in
[FEATURES.md](FEATURES.md). Test commands do not start the bot.

## Render

Deploy the bot and Mini App with [render.yaml](render.yaml), and create hosted
PostgreSQL separately. Set `DATABASE_URL` manually in a private `.env` file;
Render Secret Files are read from `/etc/secrets/.env`. The Mini App URL is assigned
automatically. See [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) for setup and paid-resource details.

## Storefront and administration features

See [FEATURES.md](FEATURES.md) for stock/price alerts, favorites, scoped staff roles,
ticket conversations, coupons, loyalty, compared financial reports, recurring
health schedules and the Telegram Mini App. On Render, the Mini App URL is detected
automatically and the bot menu is configured at startup. [render.yaml](render.yaml)
provides an optional Docker deployment blueprint; it requires your existing secrets.

An Ubuntu/Debian VPS with `systemd` remains an alternative deployment option.

## Required environment variables

- `API_ID`
- `API_HASH`
- `ADMIN_ID`
- `DEVELOPER_ID`: required; restricts `/update` to this ID.
- `BOT_TOKEN`
- `SESSION_ENCRYPTION_KEY`
- `DATABASE_URL`: PostgreSQL connection URL, entered manually in `.env`.

The application reads Render's `/etc/secrets/.env`, then `.env` beside `config.py`.
Values already set in the process environment take precedence. Keep `.env` out of Git.

For a brand-new database only, generate `SESSION_ENCRYPTION_KEY` with:

```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

## Optional environment variables

- `PORT`: defaults to `10000`.
- `HOST`: defaults to `0.0.0.0`.
- `BACKUP_DIR`: defaults to `database/backups`.
- `BACKUP_RETENTION_DAYS`: number of backup days to retain (default: `14`).
- `LOG_LEVEL`: `INFO` by default; use `DEBUG` temporarily when diagnosing an issue.
- `PG_DUMP_PATH`: optional full path to `pg_dump` when it is not available on `PATH`.

## Operations

At startup the bot creates all database tables and starts hourly operational
checks. A PostgreSQL backup is created once per calendar day with `pg_dump`
and sent to the primary developer (`ADMIN_ID`). The **النسخ الاحتياطي اليومي**
button creates and sends a recovery bundle immediately and keeps daily backups
enabled. The bundle contains the PostgreSQL dump and restore instructions only;
obtain `SESSION_ENCRYPTION_KEY` independently from the server secret store
before starting a restored instance. The
administrator panel contains **حالة التشغيل** for active users, open tickets,
pending withdrawals, active jobs, and database size.

The project requires PostgreSQL; SQLite is not supported.

## Operations center and account management

The main menu now includes **مركز المهام**. Import, manual health checks,
posting, creation, backup and restore attempts retain their
status and progress in PostgreSQL. Cancellation is cooperative at checkpoints;
already committed account/financial changes are preserved. During a conversation
waiting for input, use its existing cancel button too. Posting sleeps check job
cancellation every five seconds. Interrupted jobs remain visible after restart;
only the existing persisted posting service resumes, with a new tracked attempt.
Backup/restore jobs cannot be cancelled midway from the menu.

**عرض الحسابات / إعدادات الحساب → إدارة كلمات 2FA** shows scheduled changes,
attempts, failure reasons and completed history. Outcome notifications contain
no passwords. The stored password can be displayed only after an explicit
confirmation in the current owner's private conversation; renters and global
administrators have no ownership bypass. A stored password may have changed
outside the bot. **تنظيم الحسابات** adds private labels/folders, phone/username/name
search and country (calling-code based), health and ownership filters. These
labels do not modify Telegram profiles. Profile search uses the latest health
check data, so unchecked accounts may not have a username/name yet.

**لوحة المطور → مراجعة السحب والاسترداد** permits rejection with a reason and
an atomic refund. Rejection competes with paid confirmation on the same request;
only one succeeds. The refund is a separate `withdrawal_refund` ledger entry.
**عرض الحسابات → إيجاراتي والتجديد** shows remaining time and creates a ten-minute
renewal quote with the price before confirmation. Repeated confirmations do not
charge twice. Expired/changed leases and known unhealthy inventory are rejected.
Reminders run every minute for the last day/hour and expiration, with persistent
deduplication and retry. Renewal invalidates unsent reminders for the old end date.

**لوحة المطور → مراقبة النسخ والاستعادة** records backup size, creation and
delivery status separately, and queues failure alerts. To enable real restore
testing, set `RESTORE_TEST_ADMIN_URL` to a PostgreSQL maintenance connection on
an isolated test server, with permission to create/drop databases. Matching
`pg_dump`/`pg_restore` executables must be installed. Each test creates its own
randomly named database, restores in a transaction, reads required table counts,
and drops only that database afterward. It never restores in-place into the
production database. A hard process/server kill may leave a temporary database
behind; interrupted tests remain marked as such. This validates restoreability,
not Telegram connectivity or possession of the external session-encryption key.

Optional end-to-end test: `PLATFORM_TEST_DATABASE_URL` must point to an **empty
isolated PostgreSQL database**. `tests/test_platform_database.py` exercises money
movement races, 2FA outcomes with mocked Telegram, and a real dump/restore cycle.

## User financial statement

**نشاطي** opens a paginated, owner-only wallet statement with transaction details,
type filters, last 7/30/90 days or all dates, identifier search, and a support
button that includes the operation identifier in the saved ticket. The old
activity log remains accessible from the statement. `L…` identifies a committed
ledger movement; `P…` identifies a payment order and remains searchable after
payment. A credited order is shown only once, as its ledger entry.

Before/after balances use the stored ledger amount and ending balance, never
today's balance. Pending payment orders have no invented balance snapshots.
Withdrawal status comes from the withdrawal request; its debit occurred when
the request was created, not when an administrator marks it paid. Refund ledger
entries are shown separately; this feature does not automatically refund or
reject payments/withdrawals. All displayed amounts are wallet dollars and
historical timestamps use the database's existing timezone convention.

New transfers and auction sales record their fees inside the balance transaction.
Historical fees that were not recorded remain unknown; older missing ledger
movements are not reconstructed. The new fee column and indexes are created
automatically on startup. The direct balance setter now also records a ledger
movement. This change does not alter prices, commissions, or user balances.

Optional integration test: set `STATEMENT_TEST_DATABASE_URL` to an **empty,
isolated PostgreSQL test database**, then run `tests/test_statement_database.py`.
It creates synthetic fixtures and never contacts Telegram or payment providers.

## Account health

**عرض الحسابات → صحة الحسابات** and **إعدادات الحساب → صحة الحسابات**
provide individual/bulk checks and persisted profile, 2FA, group/channel counts,
and last-attempt/last-confirmed timestamps (UTC). Counts are marked partial when
the 1,000-dialog or time limit is reached. The scanner only reads Telegram data;
it does not log in, change passwords, log out sessions, or message SpamBot.
The 2FA flag is informational, not a failure. Telegram's account restriction
flag is not proof of a spam limitation; spam status is explicitly unverified.

The background monitor checks due accounts every six hours, processing at most
50 per pass, with two concurrent checks maximum across manual/background work.
Large inventories can take longer. Manual repeats reuse checks less than one
minute old and respect persisted Telegram flood waits. Network failures retry
after 15 minutes and retain the last confirmed status. New/replaced sessions
are independent; unchecked accounts remain eligible.

Confirmed unusable sessions are excluded from service pools and posting; rental
allocation and its availability count exclude confirmed faults for the exact
inventory session inspected. Confirmed revoked installations are now removed
from live account storage, including matching purchased copies and obsolete
credentials, so the phone can be registered again using a new valid session.
Network failures and flood waits never delete an account. Dollar balances and
financial history remain intact. See [session cleanup](docs/SESSION_LIFECYCLE.md).
A successful recheck of other health faults restores eligibility, but does
not restart stopped posting jobs. Ownership and active rental access are checked
for every health callback. Only current owners/renters receive status-change
notices; failed deliveries retry on a subsequent monitor pass. The first healthy
check is silent. Health tables are created automatically by `init_db()` and are
included in the existing PostgreSQL backups.
