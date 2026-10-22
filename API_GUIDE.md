# Paid External API

The API reuses the same backend/business logic used by the Telegram bot and Mini App. Access is tied to the Telegram user that owns the API key and requires an active monthly or yearly API subscription.

## Configuration

- `API_BASE_URL` (optional): public API root, for example `https://example.com/external/v1`.
- If it is not set, the server derives the URL from `RENDER_EXTERNAL_URL` or `MINI_APP_URL`.
- Subscription prices are stored in `settings` as `api_monthly_price` and `api_yearly_price` and can be changed by the developer from **قسم API**.
- Default prices on a fresh database are `$10.00` monthly and `$100.00` yearly.

## Authentication

Create an API key from **قسم API** after purchasing a subscription. The raw key is shown once. Only its SHA-256 hash is stored in the database.

Send every request with:

```http
Authorization: Bearer sk_live_...
```

The default limit is 120 completed requests per minute per key. Do not expose the API key in browser JavaScript; call the API from your own server/backend.

## Main endpoints

```text
GET  /external/v1/status
GET  /external/v1/services
GET  /external/v1/platform/console
POST /external/v1/platform/console/start
POST /external/v1/platform/console/click
POST /external/v1/platform/console/answer
GET|POST /external/v1/platform/...
GET|POST /external/v1/core/...
```

All `POST /external/v1/platform/...` requests require a unique `X-Idempotency-Key` containing 16-128 letters, digits, `_` or `-`. Replaying the same key with the same body returns the saved result; reusing it for another body is rejected.

## Run any bot section through the console API

1. `GET /services` returns the service catalog and keys such as `store`, `accounts`, `automation`, `promotions`, and other sections the owner is allowed to access.
2. Start a section:

```http
POST /external/v1/platform/console/start
X-Idempotency-Key: 01HZZZZZZZZZZZZZZZZZZZZZ
Content-Type: application/json

{"section":"store"}
```

3. The response contains messages, buttons and (when a handler is waiting for text) a `prompt` token.
4. Press a returned button token:

```json
{"token":"BUTTON_TOKEN"}
```

with `POST /external/v1/platform/console/click`.
5. Reply to a prompt with `POST /external/v1/platform/console/answer`:

```json
{"prompt":"PROMPT_TOKEN","text":"user input"}
```

Paid API console sessions are isolated from Mini App console sessions. This lets a trusted server-side client execute sensitive workflows without weakening the normal web console restrictions.

## Direct core API examples

- `GET /core/catalog`: available number catalog.
- `POST /core/purchase/quote` then `/core/purchase/confirm`: purchase.
- `POST /core/rental/quote` then `/core/rental/confirm`: rental.
- `GET /core/accounts`: owned accounts.
- `GET /core/account/{phone}/status`: account status.
- `POST /core/account/{phone}/health`: request health check.
- `GET /core/tickets`, `POST /core/tickets`, `POST /core/ticket/{id}/message`: support.
- `GET /core/automation/rules`, `POST /core/automation/rule/save|toggle|delete`: automation rules.
- `GET /core/automation/jobs`, `POST /core/automation/job/save|start|pause|delete`: automation jobs.

The `/platform/...` gateway additionally exposes the existing native platform endpoints for promotions, funding, preferences, tasks and the generic service console.
