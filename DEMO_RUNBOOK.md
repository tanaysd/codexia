# Codexia Demo Runbook

## Narrative (8–10 min flow)
1. **Morning Brief** – open the dashboard and pick a claim.
2. **Assess** – run `/v1/assess` to get drivers and citations.
3. **Plan** – invoke `/v1/plan` for recoding or appeal strategy.
4. **Act** – call `/v1/act` to produce the corrected claim or appeal letter and write an audit entry.
5. **Sidebar** – show the extension at `public/demo/mock.html`.
6. **Close** – emphasize faster claims, compliance, and audit trail.

## Preflight Steps
- Verify Python and Node versions: `python3 --version` and `node --version`.
- Install deps: `make bootstrap`.
- Build vector index: `python -m packages.backend.rag.indexer` or run reset script below.
- Start services:
  - Backend: `cd packages/backend && uvicorn main:app --reload`.
  - Frontend: `cd packages/frontend && npm start`.
  - Extension: load Unpacked in Chrome.

## Reset Script
```bash
./scripts/reset_demo.sh
```

## Live Commands
```bash
# Health check
curl -s localhost:8000/healthz | jq

# Assess
curl -s -X POST localhost:8000/v1/assess -d '{"claim_id":1}' | jq

# Plan
curl -s -X POST localhost:8000/v1/plan -d '{"claim_id":1}' | jq

# Act
curl -s -X POST localhost:8000/v1/act -d '{"claim_id":1}' | jq
```

## Fallback Playbook
- Backend down → restart uvicorn.
- Empty citations → rerun reset script.
- CORS error → check `ALLOWED_ORIGINS`.
- 429 rate limit → raise `RATE_LIMIT_RPS`.
- Extension not mounting → reload Unpacked and open `mock.html`.
- Audit missing → confirm Act was called.

## Dry-Run Checklist (night before)
- Tests green.
- Vector index exists.
- `/healthz` ready.
- Morning Brief shows items.
- One Assess → Plan → Act round trip.
- Audit log present.
- Extension sidebar works.
