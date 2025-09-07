#!/usr/bin/env bash
set -euo pipefail

rm -rf ./var/vector
rm -rf ./var/audit

python - <<'PY'
from packages.backend.rag.indexer import build_index
build_index("packages/backend/data/policies", "./var/vector")
print("OK: vector index rebuilt")
PY

echo "OK: audit dir will be recreated on first /v1/act"
