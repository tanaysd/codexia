#!/usr/bin/env bash
set -euo pipefail

echo "🚀 Starting Codexia RCM Copilot..."
echo ""

# Check if setup has been run
if [ ! -d "packages/backend/.venv" ] || [ ! -d "packages/frontend/node_modules" ] || [ ! -d "var/vector" ]; then
    echo "⚠️  Setup required. Running initial setup..."
    make setup
    echo ""
fi

echo "🏥 Starting services..."
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop both services"
echo ""

# Start both services with proper signal handling
trap 'echo ""; echo "🛑 Stopping services..."; kill 0; exit 0' INT

(cd packages/backend && . .venv/bin/activate && uvicorn app:app --reload --host 0.0.0.0 --port 8000) &
(cd packages/frontend && npm run dev) &

wait