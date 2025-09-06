# Codexia Monorepo

This repository hosts multiple packages:

- `packages/contracts` – shared TypeScript contracts.
- `packages/backend` – backend service.
- `packages/frontend` – console web app.
- `packages/extension` – sidebar extension.

Additional directories:

- `infra` – infrastructure configuration (e.g. docker-compose).
- `scripts` – reusable scripts.

## Tooling

Common tooling is configured at the root:

- **Lint**: `npm run lint`
- **Test**: `npm test`
- **Typecheck**: `npm run typecheck`
- **Docker**: `docker build -t codexia .`

Continuous integration runs these commands via GitHub Actions.

## Ops/Security

The backend sets strict headers on every response:
`X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy` and `Cache-Control`.
Enable `Strict-Transport-Security` by setting `ENABLE_HSTS=true` **only** when serving behind TLS.

Payload and rate limits are configurable via environment variables such as
`MAX_PAYLOAD_BYTES` and `RATE_LIMIT_RPS`. Metrics are exposed in Prometheus
format at `/metrics` and include request counts, latencies and rate-limit drops.
