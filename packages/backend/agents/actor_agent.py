from __future__ import annotations
from typing import Dict, Any, List
from hashlib import sha256
from copy import deepcopy

from ..tools.templates import template_corrected_claim, template_appeal_letter


def _sha256(obj: Any) -> str:
    import json
    b = json.dumps(obj, separators=(",", ":"), sort_keys=True).encode("utf-8")
    return sha256(b).hexdigest()


def act_on_plan(claim: Dict, plan_result: Dict, evidence: List[Dict] | None = None) -> Dict[str, Any]:
    """Apply the chosen plan to the claim and return artifact details."""
    claim_in = deepcopy(claim)
    plans = plan_result.get("plans") or []
    chosen = None
    for p in plans:
        if p.get("type") == "recoding":
            chosen = p
            break
    if chosen is None and plans:
        chosen = plans[0]
    if not chosen:
        raise ValueError("No plan provided")

    if chosen["type"] == "recoding":
        actions = chosen.get("actions") or []
        corrected = template_corrected_claim(claim_in, actions)
        return {
            "artifactType": "corrected_claim",
            "payload": corrected,
            "meta": {
                "input_sha256": _sha256(claim_in),
                "output_sha256": _sha256(corrected),
                "actions": actions,
                "plan_type": "recoding",
            },
        }

    reason = " / ".join([a.get("reason", "appeal") for a in chosen.get("actions", [])]) or "appeal"
    passages = evidence or []
    letter = template_appeal_letter(claim_in, reason, passages)
    return {
        "artifactType": "appeal_letter",
        "payload": letter,
        "meta": {
            "input_sha256": _sha256(claim_in),
            "output_sha256": _sha256(letter),
            "actions": chosen.get("actions") or [],
            "plan_type": "appeal",
        },
    }
