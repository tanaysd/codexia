from fastapi.testclient import TestClient
import os, sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))

from packages.backend.rag.indexer import build_index
from packages.backend.app import app

CASE_MOD59 = {
  "claimId": "CLM-1001",
  "payer": {"name": "UnitedHealthcare", "planId": "UHC-GOLD-CA", "state": "CA"},
  "patient": {"dob": "1962-05-14", "age": 63, "sex": "F"},
  "provider": {"npi": "1093817465", "siteOfService": "11"},
  "lines": [
    {"cpt": "97012", "dx": ["M25.511"], "modifiers": [""], "units": 1, "charge": 180.00},
    {"cpt": "97110", "dx": ["M25.511"], "modifiers": [""], "units": 1, "charge": 190.00}
  ],
  "attachments": [{"type":"progress_note", "id":"doc_123"}],
  "history": [{"ts":"2025-09-05T10:00:00Z","event":"created"}],
  "notes": ["Therapeutic exercise same session; distinct procedural service not indicated in line 1."]
}


ROOT = Path(__file__).resolve().parents[2]
POLICY_DIR = str(ROOT / "data/policies")


def test_assess_stub(tmp_path):
    vector_dir = tmp_path / "vector"
    build_index(POLICY_DIR, str(vector_dir))
    os.environ["VECTOR_PATH"] = str(vector_dir)
    c = TestClient(app)
    r = c.post("/v1/assess", json=CASE_MOD59)
    assert r.status_code == 200
    data = r.json()
    assert 0.0 <= data["risk"] <= 1.0
    assert isinstance(data["drivers"], list)
    assert isinstance(data["evidence"], list)


def test_plan_and_act_stub(tmp_path):
    vector_dir = tmp_path / "vector"
    build_index(POLICY_DIR, str(vector_dir))
    os.environ["VECTOR_PATH"] = str(vector_dir)
    c = TestClient(app)
    assess = c.post("/v1/assess", json=CASE_MOD59).json()
    plan = c.post("/v1/plan", json={"claim": CASE_MOD59, "assessment": assess}).json()
    for p in plan.get("plans", []):
        for act in p.get("actions", []):
            if act.get("replaceDx") is None:
                act["replaceDx"] = {"from": "", "to": ""}
    assert "plans" in plan and len(plan["plans"]) >= 1
    act = c.post("/v1/act", json={"claim": CASE_MOD59, "plan": plan})
    assert act.status_code == 200
    payload = act.json()["payload"]
    assert "lines" in payload or "markdown" in payload

