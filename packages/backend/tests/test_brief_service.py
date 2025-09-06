import os, sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[3]))

from packages.backend.rag.indexer import build_index
from packages.backend.services import compute_brief

POLICY_DIR = "packages/backend/data/policies"
EXAMPLES_DIR = "packages/backend/data/examples/claims"


def test_compute_brief(tmp_path):
    vector_dir = tmp_path / "vector"
    build_index(POLICY_DIR, str(vector_dir))
    out1 = compute_brief("U1", "2025-09-06", str(vector_dir), EXAMPLES_DIR)
    out2 = compute_brief("U1", "2025-09-06", str(vector_dir), EXAMPLES_DIR)

    assert out1["highlights"]
    assert len(out1["queue"]) >= 4
    top = out1["queue"][0]
    for key in ["claimId", "score", "expDeltaUsd", "why", "etaMin"]:
        assert key in top
    assert top["why"][0] in {"modifier_missing", "dx_unspecific", "doc_missing", "dx_incompatibility"}
    assert out1["queue"] == out2["queue"]
