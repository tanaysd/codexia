import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))

from packages.backend.rag.indexer import build_index
from packages.backend.rag.retrieve import semantic_search, query_policy_for_claim_context

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
        "Therapeutic exercise same session; distinct procedural service not indicated in line 1."
    ],
}


ROOT = Path(__file__).resolve().parents[1]
POLICY_DIR = str(ROOT / "data/policies")


def test_build_and_query(tmp_path):
    vector_dir = tmp_path / "vector"
    _, meta = build_index(POLICY_DIR, str(vector_dir))
    assert os.path.exists(vector_dir / "index.faiss")
    assert os.path.exists(vector_dir / "meta.json")
    assert meta["vector_dim"] == 384

    q1 = "modifier 59 with 97012 and 97110 same date of service"
    r1 = semantic_search(q1, 5, str(vector_dir))
    assert any(p["clause_id"] == "UHC-LCD-123 §3b" for p in r1["results"])

    q2 = "UnitedHealthcare 97012 97110 modifier 59"
    r2 = semantic_search(q2, 3, str(vector_dir))
    clauses = [p["clause_id"] for p in r2["results"][:3]]
    assert "UHC-LCD-123 §3b" in clauses

    r3 = semantic_search(q2, 5, str(vector_dir))
    r4 = semantic_search(q2, 5, str(vector_dir))
    assert r3 == r4

    claim_ret = query_policy_for_claim_context(CASE_MOD59, 3, str(vector_dir))
    top_clause = claim_ret["results"][0]["clause_id"]
    assert "UHC-LCD-123" in top_clause or "Kaiser-ACL-22" in top_clause
