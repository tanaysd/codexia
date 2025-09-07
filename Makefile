.PHONY: bootstrap lint typecheck test build up down setup-backend setup-frontend setup-vector setup dev dev-bg backend frontend stop reset clean health

bootstrap:
	@echo "== bootstrap =="
	npm ci
	[ -d packages/backend ] && (cd packages/backend && npm ci || true)
	[ -d packages/frontend ] && (cd packages/frontend && npm ci || true)
	[ -d packages/extension ] && (cd packages/extension && npm ci || true)
	[ -d packages/contracts ] && (cd packages/contracts && npm ci || true)
	[ -d packages/contracts-py ] && (cd packages/contracts-py && python3 -m pip install -U pip && pip install -e . && pip install pytest mypy ruff black || true)

setup-backend:
	@echo "== Setting up backend =="
	cd packages/backend && python3 -m venv .venv
	cd packages/backend && . .venv/bin/activate && pip install -r requirements.txt
	@echo "Backend setup complete!"

setup-frontend:
	@echo "== Setting up frontend =="
	cd packages/frontend && npm install
	@echo "Frontend setup complete!"

setup-vector:
	@echo "== Building vector index =="
	cd packages/backend && . .venv/bin/activate && python -c "from rag.indexer import build_index; build_index('data/policies', '../../var/vector'); print('Vector index built successfully!')"

setup: setup-backend setup-frontend setup-vector
	@echo "\n🎉 Codexia setup complete!"
	@echo "\nTo start the demo:"
	@echo "  make dev"
	@echo "\nOr start services individually:"
	@echo "  make backend  # Terminal 1"
	@echo "  make frontend # Terminal 2"

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

backend:
	@echo "🚀 Starting backend server..."
	cd packages/backend && . .venv/bin/activate && uvicorn app:app --reload --host 0.0.0.0 --port 8000

frontend:
	@echo "🚀 Starting frontend server..."
	cd packages/frontend && npm run dev

dev:
	@echo "🚀 Starting Codexia in development mode..."
	@echo "Backend will start on http://localhost:8000"
	@echo "Frontend will start on http://localhost:5173"
	@echo "\nPress Ctrl+C to stop both services\n"
	@(\
		trap 'kill 0' INT; \
		(cd packages/backend && . .venv/bin/activate && uvicorn app:app --reload --host 0.0.0.0 --port 8000) & \
		(cd packages/frontend && npm run dev) & \
		wait \
	)

dev-bg:
	@echo "🚀 Starting Codexia services in background..."
	cd packages/backend && . .venv/bin/activate && uvicorn app:app --reload --host 0.0.0.0 --port 8000 &
	cd packages/frontend && npm run dev &
	@echo "✅ Services started in background"
	@echo "Backend: http://localhost:8000"
	@echo "Frontend: http://localhost:5173"
	@echo "\nTo stop: make stop"

stop:
	@echo "🛑 Stopping Codexia services..."
	@pkill -f "uvicorn.*app:app" || true
	@pkill -f "vite.*dev" || true
	@echo "✅ Services stopped"

reset:
	@echo "🔄 Resetting demo environment..."
	./scripts/reset_demo.sh
	@echo "✅ Demo reset complete!"

clean:
	@echo "🧹 Cleaning up..."
	rm -rf packages/frontend/node_modules
	rm -rf packages/backend/.venv
	rm -rf var/vector
	rm -rf var/audit
	@echo "✅ Cleanup complete!"

health:
	@echo "🏥 Checking service health..."
	@curl -s http://localhost:8000/healthz | jq . || echo "❌ Backend not running"
	@curl -s http://localhost:5173 > /dev/null && echo "✅ Frontend running" || echo "❌ Frontend not running"
