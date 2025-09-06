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
