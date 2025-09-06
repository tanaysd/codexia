import os, sys, time
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))

from fastapi.testclient import TestClient
from packages.backend.rag.indexer import build_index

POLICY_DIR = "packages/backend/data/policies"
CLAIM = {
    "claimId": "CLM-1001",
    "payer": {"name": "UnitedHealthcare", "planId": "UHC-GOLD-CA", "state": "CA"},
    "patient": {"dob": "1962-05-14", "age": 63, "sex": "F"},
    "provider": {"npi": "1093817465", "siteOfService": "11"},
    "lines": [
        {"cpt": "97012", "dx": ["M25.50"], "modifiers": [""], "units": 1, "charge": 180.0},
        {"cpt": "97110", "dx": ["M25.50"], "modifiers": [""], "units": 1, "charge": 190.0},
    ],
    "attachments": [{"type": "progress_note", "id": "doc_123"}],
    "history": [{"ts": "2025-09-05T10:00:00Z", "event": "created"}],
    "notes": [
        "Therapeutic exercise same session; distinct procedural service not indicated in line 1.",
    ],
}



def test_end_to_end(tmp_path):
    os.environ["VECTOR_PATH"] = str(tmp_path / "vector")
    from packages.backend.app import app  # import after env var

    build_index(POLICY_DIR, os.environ["VECTOR_PATH"])
    c = TestClient(app)

    start = time.perf_counter()
    assess = c.post("/v1/assess", json=CLAIM).json()
    plan = c.post("/v1/plan", json={"claim": CLAIM, "assessment": assess}).json()
    act = c.post("/v1/act", json={"claim": CLAIM, "plan": plan}).json()
    brief = c.get("/v1/brief", params={"user_id": "U1", "date": "2025-09-06"}).json()
    elapsed = time.perf_counter() - start

    assert act["artifactType"] in {"corrected_claim", "appeal_letter"}
    assert isinstance(act["payload"], dict)
    assert len(brief["queue"]) >= 4
    assert 0.0 <= brief["queue"][0]["score"] <= 1.0
    assert any(item["claimId"] == CLAIM["claimId"] for item in brief["queue"])
    assert elapsed < 0.5
