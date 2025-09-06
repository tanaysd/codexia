import sys, pathlib; sys.path.append(str(pathlib.Path(__file__).resolve().parents[3]))
from packages.backend.tools.code_rules import modifier_rules, suggest_recoding
from packages.backend.tools.templates import template_corrected_claim, template_appeal_letter

case_mod59 = {
    "claimId": "C1",
    "payer": {"name": "Demo"},
    "provider": {"siteOfService": "11"},
    "lines": [
        {"cpt": "97012", "dx": ["M25.50"], "modifiers": []},
        {"cpt": "97110", "dx": ["M25.50"], "modifiers": []},
    ],
}


def test_template_corrected_claim_pure_and_appends():
    issues = modifier_rules(case_mod59)
    actions = suggest_recoding(case_mod59, issues)
    new_claim = template_corrected_claim(case_mod59, actions)
    # input untouched
    assert "59" not in case_mod59["lines"][0]["modifiers"]
    # modifier added to first line
    assert "59" in new_claim["lines"][0]["modifiers"]
    assert "59" not in new_claim["lines"][1]["modifiers"]


def test_template_appeal_letter():
    passages = [
        {"clause_id": "UHC-LCD-123 §3b", "text": "Traction with exercise policy."},
        {"clause_id": "Med-XYZ §1", "text": "Sample clause."},
    ]
    letter = template_appeal_letter(case_mod59, "modifier 59 missing", passages)
    md = letter["markdown"]
    assert "C1" in md and "Demo" in md
    assert "UHC-LCD-123 §3b" in md and "Med-XYZ §1" in md
    assert len(md.split()) < 320
