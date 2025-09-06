from __future__ import annotations

import json
import os
from datetime import date, datetime
from typing import Any, Dict, List

from ..agents.assessor_agent import assess_claim
from ..core.config import Settings

_PS_MAP = {
    "modifier_missing": 0.75,
    "dx_unspecific": 0.55,
    "doc_missing": 0.50,
    "dx_incompatibility": 0.45,
}
_EFFORT_MAP = {
    "modifier_missing": 2,
    "dx_unspecific": 5,
    "doc_missing": 6,
    "dx_incompatibility": 8,
}


def _deadline_score(base: date, dl: str | None) -> float:
    if not dl:
        return 0.2
    try:
        d = datetime.fromisoformat(dl).date()
    except Exception:
        return 0.2
    diff = (d - base).days
    if diff <= 3:
        return 1.0
    if diff <= 7:
        return 0.6
    return 0.3


def _user_fit(user_id: str, issue: str) -> float:
    if user_id == "U1" and issue == "modifier_missing":
        return 0.8
    if user_id == "U2" and issue == "doc_missing":
        return 0.8
    return 0.5


def compute_brief(user_id: str, date: str, vector_dir: str, examples_dir: str) -> Dict[str, Any]:
    """Returns BriefResult-like dict with highlights[] and queue[]. Deterministic."""
    settings = Settings()
    base_date = datetime.fromisoformat(date).date()

    items: List[Dict[str, Any]] = []
    for fname in sorted(os.listdir(examples_dir)):
        if not fname.endswith('.json'):
            continue
        path = os.path.join(examples_dir, fname)
        with open(path, 'r', encoding='utf-8') as f:
            raw = json.load(f)
        exp_delta = float(raw.pop('expDeltaUsd', 120))
        deadline = raw.pop('deadline', None)
        claim = raw

        assess = assess_claim(claim, vector_dir)
        drivers = assess.get('drivers') or []
        primary = drivers[0]['issue'] if drivers else 'other'
        p_success = _PS_MAP.get(primary, 0.5)
        effort = _EFFORT_MAP.get(primary, 5)

        ev = assess.get('evidence') or []
        clause = None
        if ev:
            clause = ev[0].get('clauseId') or ev[0].get('source')
        why: List[str] = [primary]
        if clause:
            why.append(clause)

        delta_norm = min(exp_delta / 1000.0, 1.0)
        feas = p_success / effort
        urg = _deadline_score(base_date, deadline)
        fit = _user_fit(user_id, primary)
        score = (
            settings.W_DELTA * delta_norm
            + settings.W_FEAS * feas
            + settings.W_URG * urg
            + settings.W_FIT * fit
        )

        item: Dict[str, Any] = {
            'claimId': claim.get('claimId', fname.rsplit('.', 1)[0]),
            'score': score,
            'expDeltaUsd': exp_delta,
            'why': why,
            'etaMin': effort,
        }
        if deadline:
            item['deadline'] = deadline
        items.append(item)

    items.sort(key=lambda x: (-x['score'], -x['expDeltaUsd'], x['claimId']))

    highlights = [
        "UHC-LCD-123 remains effective 2024-01-01 →",
        "CMS-NCD-456 guidance updated 2024-05-15 →",
    ]
    return {'highlights': highlights, 'queue': items}
