from fastapi.testclient import TestClient
from pathlib import Path
import json

from packages.backend.app import app
from packages.backend.core.config import Settings

CASE = {
    "claimId": "CLM-1001",
    "payer": {"name": "UnitedHealthcare", "planId": "UHC-GOLD-CA", "state": "CA"},
    "patient": {"dob": "1962-05-14", "age": 63, "sex": "F"},
    "provider": {"npi": "1093817465", "siteOfService": "11"},
    "lines": [
        {"cpt": "97012", "dx": ["M25.50"], "modifiers": [""], "units": 1, "charge": 180.00},
        {"cpt": "97110", "dx": ["M25.50"], "modifiers": [""], "units": 1, "charge": 190.00},
    ],
    "attachments": [{"type": "progress_note", "id": "doc_123"}],
    "history": [{"ts": "2025-09-05T10:00:00Z", "event": "created"}],
    "notes": [
        "Therapeutic exercise same session; distinct procedural service not indicated in line 1."
    ],
}


def test_act_writes_audit(tmp_path, monkeypatch):
    monkeypatch.setenv("AUDIT_PATH", str(tmp_path / "audit"))
    c = TestClient(app)

    assess = c.post("/v1/assess", json=CASE).json()
    plan = c.post("/v1/plan", json={"claim": CASE, "assessment": assess}).json()

    res = c.post("/v1/act", json={"claim": CASE, "plan": plan, "assessment": assess})
    assert res.status_code == 200
    data = res.json()
    assert data["artifactType"] in ("corrected_claim", "appeal_letter")

    audit_dir = Path(Settings().AUDIT_PATH)
    files = list(audit_dir.glob("*.jsonl"))
    assert files, "no audit file written"
    content = files[0].read_text(encoding="utf-8").strip().splitlines()
    assert len(content) >= 1
    rec = json.loads(content[-1])
    assert rec["kind"] == "act"
    assert "sha256" in rec and len(rec["sha256"]) == 64
