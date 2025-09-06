from __future__ import annotations

from typing import Any, Dict, List, Tuple

from ..tools.code_rules import normalize_codes, icd_cpt_validate, modifier_rules
from ..rag.retrieve import query_policy_for_claim_context, semantic_search
from ..models import score_risk

ISSUE_MAP = {
    "modifier_missing": "modifier_missing",
    "dx_unspecific": "dx_unspecific",
    "doc_missing": "doc_missing",
    "dx_incompatibility": "dx_incompatibility",
    "format_error": "other",
    "sos_restriction": "sos_restriction",
}

PRIORITY = [
    "modifier_missing",
    "dx_incompatibility",
    "doc_missing",
    "dx_unspecific",
    "sos_restriction",
    "other",
]
PRIORITY_IDX = {v: i for i, v in enumerate(PRIORITY)}


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


def _build_features(claim: Dict[str, Any], issues: List[Dict[str, Any]]) -> Dict[str, float]:
    return {
        "f_modifier_missing": int(any(i["issue"] == "modifier_missing" for i in issues)),
        "f_dx_unspecific": int(any(i["issue"] == "dx_unspecific" for i in issues)),
        "f_doc_missing": int(any(i["issue"] == "doc_missing" for i in issues)),
        "f_dx_incompatibility": int(any(i["issue"] == "dx_incompatibility" for i in issues)),
        "f_lines": min(5, len(claim.get("lines", []))) / 5.0,
    }


def _driver_candidates(issues: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    drivers: List[Dict[str, Any]] = []
    src_issues: List[Dict[str, Any]] = []
    for iss in issues:
        mapped = ISSUE_MAP.get(iss["issue"])
        if not mapped:
            continue
        drivers.append({"line": iss.get("line", 0), "issue": mapped, "why": iss.get("why", "")})
        src_issues.append(iss)
    pairs = list(zip(drivers, src_issues))
    pairs.sort(key=lambda p: (PRIORITY_IDX[p[0]["issue"]], p[0]["line"], p[0]["why"]))
    pairs = pairs[:3]
    return [d for d, _ in pairs], [s for _, s in pairs]


def _query_for_driver(driver: Dict[str, Any], issue_obj: Dict[str, Any], claim: Dict[str, Any]) -> str:
    issue = driver["issue"]
    cpts = [ln.get("cpt", "") for ln in claim.get("lines", [])]
    pair = cpts[:2]
    if issue == "modifier_missing":
        parts = ["modifier 59"] + pair
        return " ".join([p for p in parts if p])
    if issue == "dx_unspecific":
        details = issue_obj.get("details") or {}
        dx = details.get("from")
        if not dx:
            line_idx = driver.get("line", 0)
            lines = claim.get("lines", [])
            if line_idx < len(lines):
                dxs = lines[line_idx].get("dx", [])
                if dxs:
                    dx = dxs[0]
        if dx:
            return f"{dx} specificity"
        return issue_obj.get("why", "")
    if issue == "doc_missing":
        return issue_obj.get("why", "")
    if issue == "dx_incompatibility":
        parts = ["dx incompatibility"] + pair
        return " ".join([p for p in parts if p])
    if issue == "sos_restriction":
        return issue_obj.get("why", "")
    return issue_obj.get("why", "")


def assess_claim(claim: Dict, vector_dir: str, topk: int = 5) -> Dict[str, Any]:
    """Returns AssessmentResult-like dict: {risk, drivers[], evidence[]}"""
    norm_claim = normalize_codes(claim)

    issues_rules = icd_cpt_validate(norm_claim)
    issues_mods = modifier_rules(norm_claim)
    issues = _dedup(issues_rules + issues_mods)

    features = _build_features(norm_claim, issues)
    risk, _tags = score_risk(features)

    drivers, src_issues = _driver_candidates(issues)

    passages: List[Dict[str, Any]] = []
    base_ret = query_policy_for_claim_context(norm_claim, topk, vector_dir)
    passages.extend(base_ret["results"])

    for drv, iss in zip(drivers, src_issues):
        q = _query_for_driver(drv, iss, norm_claim)
        if not q:
            continue
        ret = semantic_search(q, topk, vector_dir)
        passages.extend(ret["results"])

    dedup: List[Dict[str, Any]] = []
    seen = set()
    for p in passages:
        key = (p["source"], p["clause_id"])
        if key in seen:
            continue
        seen.add(key)
        dedup.append(p)
        if len(dedup) >= topk:
            break

    evidence: List[Dict[str, Any]] = []
    for p in dedup:
        eff = {"from": p["effective_from"]}
        if p.get("effective_to"):
            eff["to"] = p["effective_to"]
        evidence.append(
            {
                "source": p["source"],
                "clauseId": p["clause_id"],
                "passage": p["text"],
                "effective": eff,
            }
        )

    return {"risk": risk, "drivers": drivers, "evidence": evidence}
