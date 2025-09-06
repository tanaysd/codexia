"""Tiny 837-like claim normaliser."""
from __future__ import annotations

from typing import Dict, List


def edi_to_claim(edi: Dict) -> Dict:
    """Normalise an 837-like dict into canonical claim dict used by tools.

    Expected shape (minimal):
    {
        "claim": {"id": str},
        "payer": {"name": str},
        "patient": {...},
        "provider": {"siteOfService": str},
        "lines": [
            {"cpt": str, "dx": [str], "modifiers": [str]}
        ]
    }
    """
    claim_section = edi.get("claim") or {}
    if "id" not in claim_section:
        raise ValueError("claim.id required")
    out = {
        "claimId": claim_section["id"],
        "payer": edi.get("payer") or {},
        "patient": edi.get("patient") or {},
        "provider": edi.get("provider") or {},
        "lines": edi.get("lines") or [],
    }
    return out
