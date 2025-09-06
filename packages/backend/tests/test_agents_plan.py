from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[3]))

from packages.backend.rag.indexer import build_index
from packages.backend.agents.assessor_agent import assess_claim
from packages.backend.agents.planner_agent import make_plan

CASE_MOD59 = {
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
        "Therapeutic exercise same session; distinct procedural service not indicated in line 1.",
    ],
}

POLICY_DIR = "packages/backend/data/policies"


def test_planner_agent(tmp_path):
    vector_dir = tmp_path / "vector"
    build_index(POLICY_DIR, str(vector_dir))
    assessment = assess_claim(CASE_MOD59, str(vector_dir))
    result = make_plan(CASE_MOD59, assessment, str(vector_dir))
    plans = result["plans"]

    assert len(plans) == 2
    types = [p["type"] for p in plans]
    assert "recoding" in types and "appeal" in types

    # recoding plan
    rec_plan = [p for p in plans if p["type"] == "recoding"][0]
    assert any(a.get("addModifier") == "59" and a.get("line") == 0 for a in rec_plan["actions"])

    # appeal plan
    appeal_plan = [p for p in plans if p["type"] == "appeal"][0]
    action = appeal_plan["actions"][0]
    assert action.get("level") == "L1"
    assert action.get("cites")
    assessment_cites = {e["clauseId"] for e in assessment.get("evidence", [])}
    assert any(c in assessment_cites for c in action["cites"])

    # ranking
    if assessment.get("drivers") and assessment["drivers"][0]["issue"] == "modifier_missing":
        assert plans[0]["type"] == "recoding"
