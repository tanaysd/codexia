from __future__ import annotations

import json
import pytest

from codexia_contracts.contracts import Claim, AssessmentResult, ClaimLine
from codexia_contracts.examples import CASE_MOD59_PY, case_mod59_wire


def test_round_trip() -> None:
    wire = case_mod59_wire()
    parsed = Claim.model_validate_json(wire)
    assert parsed == CASE_MOD59_PY


def test_risk_bounds() -> None:
    with pytest.raises(ValueError):
        AssessmentResult(claim_id="x", risk=1.5)


def test_cpt_regex() -> None:
    with pytest.raises(ValueError):
        ClaimLine(cpt="97A12", dx=["M25.50"], modifiers=[], units=1, charge=1.0)


def test_id_regex() -> None:
    bad = json.loads(case_mod59_wire())
    bad["claimId"] = "!bad"
    with pytest.raises(ValueError):
        Claim.model_validate(bad)
