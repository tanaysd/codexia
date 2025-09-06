from __future__ import annotations

from typing import Any, Dict, List

from ..tools.code_rules import (
    normalize_codes,
    icd_cpt_validate,
    modifier_rules,
    suggest_recoding,
)

ISSUE_SET = {
    "modifier_missing",
    "dx_unspecific",
    "doc_missing",
    "dx_incompatibility",
}


def _dedup(issues: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen = set()
    out = []
    for iss in issues:
        key = (iss.get("issue"), iss.get("line"), iss.get("why", ""))
        if key in seen:
            continue
        seen.add(key)
        out.append(iss)
    out.sort(key=lambda x: (x["issue"], x.get("line", 0), x.get("why", "")))
    return out


def make_plan(claim: Dict, assessment: Dict, vector_dir: str, topk: int = 5) -> Dict[str, Any]:
    """Returns PlanResult-like dict with one recoding and one appeal option"""
    norm_claim = normalize_codes(claim)
    issues = _dedup(icd_cpt_validate(norm_claim) + modifier_rules(norm_claim))

    actions = suggest_recoding(norm_claim, issues)[:2]
    plan_cite = None
    for iss in issues:
        refs = iss.get("policy_refs")
        if refs:
            plan_cite = sorted(refs)[0]
            break

    recoding_plan: Dict[str, Any] = {
        "type": "recoding",
        "actions": actions,
        "rationale": "Resolve modifier/document specificity to meet payer policy.",
    }
    if plan_cite:
        recoding_plan["cite"] = plan_cite

    top_driver = assessment.get("drivers", [])
    top_reason = top_driver[0]["issue"] if top_driver else "other"
    cites = [e["clauseId"] for e in assessment.get("evidence", [])][:2]
    appeal_plan: Dict[str, Any] = {
        "type": "appeal",
        "actions": [{"level": "L1", "reason": top_reason, "cites": cites}],
        "rationale": "Argue medical necessity per cited clauses.",
    }

    has = {iss["issue"] for iss in issues}
    score_rec = (0.15 if "modifier_missing" in has else 0.0) + (0.10 if "dx_unspecific" in has else 0.0)
    score_app = (0.15 if "doc_missing" in has else 0.0) + (0.10 if "dx_incompatibility" in has else 0.0)

    plans = [recoding_plan, appeal_plan]
    if score_app > score_rec:
        plans = [appeal_plan, recoding_plan]

    return {"plans": plans}
