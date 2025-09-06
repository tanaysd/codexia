import json
import os
import sys
from pathlib import Path

os.environ.setdefault("HF_DATASETS_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
os.environ.setdefault("HF_HUB_OFFLINE", "1")

sys.path.append(str(Path(__file__).resolve().parents[3]))

from packages.backend.rag.indexer import build_index
from packages.backend.rag.retrieve import semantic_search, query_policy_for_claim_context

ROOT = Path(__file__).resolve().parents[1]
POLICY_DIR = str(ROOT / "data/policies")


def test_rag_corpus_quality(tmp_path):
    vector_dir = tmp_path / "vec"
    build_index(POLICY_DIR, str(vector_dir), rebuild=True)

    q1 = "modifier 59 97012 97110 same date of service"
    r1 = semantic_search(q1, 5, str(vector_dir))
    clauses1 = [p["clause_id"] for p in r1["results"]]
    assert any(c in clauses1 for c in [
        "UHC-LCD-123 §3b",
        "Humana-PT-014 §2",
        "UHC-PT-222 §1",
        "Kaiser-ACL-22 §1",
        "Cigna-MED-77 §2",
    ])

    q2 = "E/M modifier 25 significant separately"
    r2 = semantic_search(q2, 3, str(vector_dir))
    clauses2 = [p["clause_id"] for p in r2["results"]]
    assert any(c == "Highmark-RAD-871 §4" for c in clauses2[:3])

    q3 = "POS 11 imaging documentation rationale"
    r3 = semantic_search(q3, 3, str(vector_dir))
    clauses3 = [p["clause_id"] for p in r3["results"]]
    assert any(c in ["BCBS-P123 §7", "Molina-MS-031 §3"] for c in clauses3[:3])

    r3_repeat = semantic_search(q3, 3, str(vector_dir))
    assert r3 == r3_repeat

    with open(ROOT / "data/examples/claims/case_mod25_e_and_m.json") as f:
        claim1 = json.load(f)
    ret1 = query_policy_for_claim_context(claim1, 5, str(vector_dir))
    assert any(p["clause_id"] == "Highmark-RAD-871 §4" for p in ret1["results"])

    with open(ROOT / "data/examples/claims/case_lab_mednec.json") as f:
        claim2 = json.load(f)
    ret2 = query_policy_for_claim_context(claim2, 5, str(vector_dir))
    assert any(p["clause_id"] == "CMS-NCD-456 §2" for p in ret2["results"])

    with open(ROOT / "data/examples/claims/case_multi_line_bundle.json") as f:
        claim3 = json.load(f)
    ret3 = query_policy_for_claim_context(claim3, 5, str(vector_dir))
    assert any(p["clause_id"] in ["UHC-PT-222 §1", "Humana-PT-014 §2"] for p in ret3["results"])
