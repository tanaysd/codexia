from __future__ import annotations

from typing import Dict, List, Tuple

from ..core.config import Settings

# Default weights for each feature
DEFAULT_WEIGHTS: Dict[str, float] = {
    "modifier_missing": 0.35,
    "dx_unspecific": 0.20,
    "doc_missing": 0.25,
    "dx_incompatibility": 0.30,
    "lines": 0.10,
}


def _resolve_weights() -> Dict[str, float]:
    """Return weights from settings if provided, else defaults."""
    try:
        settings = Settings()
        cfg = getattr(settings, "RISK_WEIGHTS", None)
        if isinstance(cfg, dict):
            merged = DEFAULT_WEIGHTS.copy()
            for k, v in cfg.items():
                if k in merged:
                    try:
                        merged[k] = float(v)
                    except Exception:
                        pass
            return merged
    except Exception:
        pass
    return DEFAULT_WEIGHTS


WEIGHTS = _resolve_weights()


def score_risk(features: Dict[str, float]) -> Tuple[float, List[str]]:
    """Compute risk score and contributing feature tags.

    Parameters
    ----------
    features: mapping of feature name prefixed with ``f_`` to numeric value.

    Returns
    -------
    (risk, driver_tags)
        risk: bounded [0,1] float
        driver_tags: list of feature names (without ``f_``) ordered by contribution
    """
    weights = WEIGHTS
    raw = 0.0
    contribs: List[Tuple[str, float]] = []
    for key, weight in weights.items():
        f_val = float(features.get(f"f_{key}", 0.0))
        contrib = f_val * weight
        raw += contrib
        if f_val > 0:
            contribs.append((key, contrib))

    risk = max(0.0, min(1.0, raw))
    contribs.sort(key=lambda x: (-x[1], x[0]))
    driver_tags = [name for name, _ in contribs]
    return risk, driver_tags
