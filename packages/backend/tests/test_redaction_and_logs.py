import logging
from fastapi.testclient import TestClient
from packages.backend.app import get_app
from packages.backend.routers import assess as assess_router

CLAIM = {
    "claimId": "C1",
    "payer": {"name": "p"},
    "patient": {"dob": "2000-01-01", "age": 1, "sex": "M"},
    "provider": {"npi": "1234567890"},
    "lines": [{"cpt": "A", "dx": ["B"], "modifiers": [], "units": 1, "charge": 1.0}],
}


def create_client(monkeypatch):
    monkeypatch.setattr(assess_router, "assess_claim", lambda *a, **k: {"risk": 0, "drivers": [], "evidence": []})
    client = TestClient(get_app())
    root = logging.getLogger()
    records: list[str] = []

    class ListHandler(logging.Handler):
        def emit(self, record):
            records.append(self.format(record))

    handler = ListHandler()
    handler.setFormatter(root.handlers[0].formatter)
    root.addHandler(handler)
    return client, records


def test_redaction_and_logs(monkeypatch, caplog):
    caplog.set_level(logging.INFO)
    c, records = create_client(monkeypatch)
    claim = dict(CLAIM)
    claim["notes"] = ["contact test@example.com"]
    r = c.post("/v1/assess", json=claim)
    assert r.status_code == 200
    joined = "\n".join(records)
    assert "[REDACTED_EMAIL]" in joined
    assert "[REDACTED_NPI]" in joined
    assert "test@example.com" not in joined
    assert "1234567890" not in joined
