import os
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[3]))

from packages.backend.rag.indexer import build_index
from packages.backend.agents.assessor_agent import assess_claim

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

ROOT = Path(__file__).resolve().parents[1]
POLICY_DIR = str(ROOT / "data/policies")


def test_assess_agent(tmp_path):
    vector_dir = tmp_path / "vector"
    build_index(POLICY_DIR, str(vector_dir))
    out1 = assess_claim(CASE_MOD59, str(vector_dir))
    out2 = assess_claim(CASE_MOD59, str(vector_dir))

    assert 0.0 <= out1["risk"] <= 1.0
    assert any(d["issue"] == "modifier_missing" and d["line"] == 0 for d in out1["drivers"])
    assert out1["drivers"] == out2["drivers"]
    assert out1["evidence"] == out2["evidence"]
    assert any(
        ev.get("clauseId") == "UHC-LCD-123 §3b" or ev.get("source") == "UHC-LCD-123.md"
        for ev in out1["evidence"]
    )
