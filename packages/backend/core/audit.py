import json
import os
from datetime import datetime
from hashlib import sha256
from .config import Settings


def audit_write(kind: str, payload: dict) -> None:
    settings = Settings()
    ts = datetime.utcnow().strftime("%Y-%m-%d")
    path = os.path.join(settings.AUDIT_PATH, f"{ts}.jsonl")
    record = {
        "ts": datetime.utcnow().isoformat() + "Z",
        "kind": kind,
        "sha256": sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest(),
        "payload": payload,
    }
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
