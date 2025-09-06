from fastapi.testclient import TestClient
from fastapi.testclient import TestClient
from packages.backend.app import get_app
from packages.backend.routers import assess as assess_router

BASE_CLAIM = {
    "claimId": "C1",
    "payer": {"name": "p"},
    "patient": {"dob": "2000-01-01", "age": 1, "sex": "M"},
    "provider": {"npi": "1234567890"},
    "lines": [{"cpt": "A", "dx": ["B"], "modifiers": [], "units": 1, "charge": 1.0}],
}


def create_client(monkeypatch, **env):
    for k, v in env.items():
        monkeypatch.setenv(k, str(v))
    monkeypatch.setattr(assess_router, "assess_claim", lambda *a, **k: {"risk": 0, "drivers": [], "evidence": []})
    return TestClient(get_app())


def test_payload_limit(monkeypatch):
    big_claim = dict(BASE_CLAIM)
    big_claim["notes"] = ["x" * 2048]
    c = create_client(monkeypatch, MAX_PAYLOAD_BYTES=1024)
    r = c.post("/v1/assess", json=big_claim)
    assert r.status_code == 413
    r = c.post("/v1/assess", json=BASE_CLAIM)
    assert r.status_code == 200
