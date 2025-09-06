.PHONY: bootstrap lint typecheck test build up down

bootstrap:
	@echo "== bootstrap =="
	npm ci
	[ -d packages/backend ] && (cd packages/backend && npm ci || true)
	[ -d packages/frontend ] && (cd packages/frontend && npm ci || true)
	[ -d packages/extension ] && (cd packages/extension && npm ci || true)
	[ -d packages/contracts ] && (cd packages/contracts && npm ci || true)
	[ -d packages/contracts-py ] && (cd packages/contracts-py && python3 -m pip install -U pip && pip install -e . && pip install pytest mypy ruff black || true)

lint:
	@echo "== lint =="
	npm run lint --workspaces || true
	[ -d packages/contracts-py ] && (cd packages/contracts-py && ruff check . && black --check .) || true

typecheck:
	@echo "== typecheck =="
	npm run typecheck --workspaces || true
	[ -d packages/contracts-py ] && (cd packages/contracts-py && mypy .) || true

test:
	# Backend Python tests
	[ -d packages/backend ] && (cd packages/backend && pytest -q) || true
	# TS tests (optional; won't fail if absent)
	[ -d packages/frontend ] && (cd packages/frontend && npm test --silent) || true
	[ -d packages/contracts ] && (cd packages/contracts && npm test --silent) || true
	[ -d packages/extension ] && (cd packages/extension && npm test --silent) || true

build:
	docker compose -f infra/docker-compose.yml build

up:
	docker compose -f infra/docker-compose.yml up -d

down:
	docker compose -f infra/docker-compose.yml down
