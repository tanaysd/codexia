from __future__ import annotations
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib
from .config import Settings


def _day_path() -> Path:
    base = Path(Settings().AUDIT_PATH)
    base.mkdir(parents=True, exist_ok=True)
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return base / f"{day}.jsonl"


def audit_write(kind: str, payload: dict) -> None:
    rec = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "kind": kind,
        "sha256": hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest(),
        "payload": payload,
    }
    path = _day_path()
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")
