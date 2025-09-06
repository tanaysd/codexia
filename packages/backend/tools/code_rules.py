"""Deterministic claim code validation and rule helpers."""
from __future__ import annotations

import re
from copy import deepcopy
from typing import Dict, List, Tuple

from .data_rules import (
    ICD10_REGEX,
    CPT_REGEX,
    MOD_REGEX,
    MODIFIER_59_REQUIRED_PAIRS,
    ICD_SPECIFICITY_SUGGESTIONS,
    SITE_OF_SERVICE_RULES,
)


# ---------------------------------------------------------------------------
# Normalisation utilities
# ---------------------------------------------------------------------------

def normalize_codes(claim: Dict) -> Dict:
    """Return a deep-copied claim with codes upper-cased and emptied items removed."""
    c = deepcopy(claim)
    for line in c.get("lines", []):
        line["dx"] = [str(d).upper().strip() for d in line.get("dx", []) if str(d).strip()]
        mods = [str(m).upper().strip() for m in line.get("modifiers", []) if str(m).strip()]
        line["modifiers"] = mods
    return c


def _pair_key(a: str, b: str) -> Tuple[str, str]:
    return tuple(sorted((a, b)))


# ---------------------------------------------------------------------------
# Validators
# ---------------------------------------------------------------------------

def icd_cpt_validate(claim: Dict) -> List[Dict]:
    """Validate CPT/ICD formatting, specificity and site-of-service notes.

    Returns a list of issue dictionaries sorted deterministically by (issue, line).
    """
    c = normalize_codes(claim)
    issues: List[Dict] = []
    pos = (c.get("provider") or {}).get("siteOfService")

    for idx, line in enumerate(c.get("lines", [])):
        cpt = line.get("cpt", "")
        if not re.match(CPT_REGEX, cpt):
            issues.append({"line": idx, "issue": "format_error", "why": f"Bad CPT {cpt}"})

        for dx in line.get("dx", []):
            if not re.match(ICD10_REGEX, dx):
                issues.append({"line": idx, "issue": "format_error", "why": f"Bad ICD {dx}"})

        for dx in line.get("dx", []):
            if dx in ICD_SPECIFICITY_SUGGESTIONS:
                issues.append(
                    {
                        "line": idx,
                        "issue": "dx_unspecific",
                        "why": f"{dx} is non-specific; consider site-specific alternative.",
                        "details": {"from": dx, "to": ICD_SPECIFICITY_SUGGESTIONS[dx][0]},
                        "policy_refs": ["Medicare-AB-2024-05 §4"],
                    }
                )
                break

        # Site-of-service notes requirement
        if pos in SITE_OF_SERVICE_RULES:
            details = line.get("details") or {}
            flags: List[str] = []
            if isinstance(details, dict):
                for k in ("flags", "tags", "flag", "tag", "type", "category"):
                    v = details.get(k)
                    if isinstance(v, str):
                        flags.append(v)
                    elif isinstance(v, list):
                        flags.extend([str(i) for i in v])
            elif isinstance(details, list):
                flags.extend([str(i) for i in details])
            elif isinstance(details, str):
                flags.append(details)

            required = SITE_OF_SERVICE_RULES[pos]["notes_required_for"]
            if any(f in required for f in flags):
                issues.append(
                    {
                        "line": idx,
                        "issue": "doc_missing",
                        "why": f"POS {pos} requires documented rationale for imaging.",
                        "policy_refs": sorted(SITE_OF_SERVICE_RULES[pos]["policy_refs"]),
                    }
                )

    issues.sort(key=lambda x: (x["issue"], x["line"]))
    return issues


def modifier_rules(claim: Dict) -> List[Dict]:
    """Detect CPT pairs that commonly require modifier -59 when billed together."""
    c = normalize_codes(claim)
    issues: List[Dict] = []
    cpts = [ln.get("cpt", "") for ln in c.get("lines", [])]

    for (a, b), meta in MODIFIER_59_REQUIRED_PAIRS.items():
        if a in cpts and b in cpts:
            idx_a, idx_b = cpts.index(a), cpts.index(b)
            target = min(idx_a, idx_b)
            has_59 = any("59" in ln.get("modifiers", []) for ln in c.get("lines", []))
            if not has_59:
                issues.append(
                    {
                        "line": target,
                        "issue": "modifier_missing",
                        "why": meta["why"],
                        "policy_refs": sorted(meta.get("policy_refs", [])),
                    }
                )
    issues.sort(key=lambda x: (x["issue"], x["line"]))
    return issues


# ---------------------------------------------------------------------------
# Suggestions
# ---------------------------------------------------------------------------

def suggest_recoding(claim: Dict, issues: List[Dict]) -> List[Dict]:
    """Generate deterministic recoding action suggestions given issue list."""
    actions: List[Dict] = []
    for iss in issues:
        if iss["issue"] == "modifier_missing":
            cite = None
            if iss.get("policy_refs"):
                cite = sorted(iss["policy_refs"])[0]
            actions.append({"line": iss["line"], "addModifier": "59", "cite": cite})
        elif iss["issue"] == "dx_unspecific":
            details = iss.get("details") or {}
            to = details.get("to")
            frm = details.get("from")
            if to and frm:
                actions.append({"line": iss["line"], "replaceDx": {"from": frm, "to": to}})
    actions.sort(key=lambda a: (0 if "addModifier" in a else 1, a["line"]))
    return actions
