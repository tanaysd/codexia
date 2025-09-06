import sys, pathlib; sys.path.append(str(pathlib.Path(__file__).resolve().parents[3]))
from packages.backend.tools.code_rules import (
    icd_cpt_validate,
    modifier_rules,
    suggest_recoding,
)


# Case 1: modifier -59 suggestion
case_mod59 = {
    "claimId": "C1",
    "payer": {"name": "Demo"},
    "provider": {"siteOfService": "11"},
    "lines": [
        {"cpt": "97012", "dx": ["M25.50"], "modifiers": []},
        {"cpt": "97110", "dx": ["M25.50"], "modifiers": []},
    ],
}


# Case 2: unspecific dx
case_dx_unspecific = {
    "claimId": "C2",
    "payer": {"name": "Demo"},
    "provider": {"siteOfService": "11"},
    "lines": [
        {"cpt": "97110", "dx": ["M25.50"], "modifiers": []}
    ],
}


# Case 3: site of service doc requirement
case_sos_note = {
    "claimId": "C3",
    "payer": {"name": "Demo"},
    "provider": {"siteOfService": "11"},
    "lines": [
        {
            "cpt": "77080",
            "dx": ["M25.511"],
            "modifiers": [],
            "details": {"flags": ["imaging_generic"]},
        }
    ],
}


def test_modifier_rules_and_suggestion_stable():
    issues = modifier_rules(case_mod59)
    assert len(issues) == 1
    assert issues[0]["issue"] == "modifier_missing"
    assert "UHC-LCD-123 §3b" in issues[0]["policy_refs"]
    # stability
    assert issues == modifier_rules(case_mod59)
    actions = suggest_recoding(case_mod59, issues)
    assert actions[0]["line"] == 0
    assert actions[0]["addModifier"] == "59"


def test_icd_unspecific_suggestion_and_stability():
    issues = icd_cpt_validate(case_dx_unspecific)
    found = [i for i in issues if i["issue"] == "dx_unspecific"]
    assert found
    assert found[0]["details"]["to"] in {"M25.512", "M25.511", "M25.519"}
    assert issues == icd_cpt_validate(case_dx_unspecific)


def test_site_of_service_doc_missing():
    issues = icd_cpt_validate(case_sos_note)
    found = [i for i in issues if i["issue"] == "doc_missing"]
    assert found
    assert "BCBS-P123 §7" in found[0]["policy_refs"]
    assert issues == icd_cpt_validate(case_sos_note)
