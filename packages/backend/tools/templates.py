"""Pure artifact generators for claim corrections and appeal letters."""
from __future__ import annotations

from copy import deepcopy
from textwrap import shorten
from typing import Dict, List


def template_corrected_claim(claim: Dict, actions: List[Dict]) -> Dict:
    """Apply recoding actions immutably and return new corrected claim dict."""
    out = deepcopy(claim)
    for act in actions:
        ln = out.get("lines", [])[act["line"]]
        if "addModifier" in act:
            mod = act["addModifier"].strip().upper()
            if mod and mod not in ln.get("modifiers", []):
                ln.setdefault("modifiers", []).append(mod)
        if "replaceDx" in act:
            frm = act["replaceDx"].get("from", "").upper()
            to = act["replaceDx"].get("to", "").upper()
            ln["dx"] = [to if d.upper() == frm else d for d in ln.get("dx", [])]
        # clean modifiers: remove empties, dedup, preserve order
        seen = set()
        cleaned: List[str] = []
        for m in ln.get("modifiers", []):
            m = m.strip().upper()
            if m and m not in seen:
                seen.add(m)
                cleaned.append(m)
        ln["modifiers"] = cleaned
    return out


def template_appeal_letter(claim: Dict, denial_reason: str, passages: List[Dict]) -> Dict:
    """Generate deterministic markdown appeal letter with policy citations."""
    claim_id = claim.get("claimId", "")
    payer = (claim.get("payer") or {}).get("name", "Payer")
    cites: List[str] = []
    bullets: List[str] = []
    for p in passages[:3]:
        cid = p.get("clause_id") or p.get("clauseId") or ""
        cites.append(cid)
        text = p.get("text") or p.get("passage") or ""
        bullets.append(f"- **{cid}**: {shorten(text.strip(), width=120, placeholder='…')}")
    body = (
        f"# Level-1 Appeal — {claim_id}\n\n"
        f"**To:** {payer}  \n"
        f"**Subject:** Reconsideration Request — Denial (“{denial_reason}”)\n\n"
        f"We request reconsideration for claim **{claim_id}**. The submitted services are supported by documentation and applicable policy guidance:\n\n"
        f"{chr(10).join(bullets)}\n\n"
        "**Requested Action:** Reverse the denial and reprocess the claim in accordance with the cited clauses.\n\n"
        "Sincerely,\nRevenue Integrity Team"
    )
    return {"markdown": body.strip(), "cites": [c for c in cites if c]}
