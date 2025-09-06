import os
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


def create_client(monkeypatch, **env):
    for k, v in env.items():
        monkeypatch.setenv(k, str(v))
    monkeypatch.setattr(assess_router, "assess_claim", lambda *a, **k: {"risk": 0, "drivers": [], "evidence": []})
    return TestClient(get_app())


def test_security_headers(monkeypatch):
    c = create_client(monkeypatch)
    r = c.get("/healthz")
    for h in ["X-Content-Type-Options", "X-Frame-Options", "Referrer-Policy", "Cache-Control"]:
        assert h in r.headers
    assert "Strict-Transport-Security" not in r.headers
    r = c.post("/v1/assess", json=CLAIM)
    for h in ["X-Content-Type-Options", "X-Frame-Options", "Referrer-Policy", "Cache-Control"]:
        assert h in r.headers
    assert r.status_code == 200

    monkeypatch.setenv("ENABLE_HSTS", "true")
    c = create_client(monkeypatch)
    r = c.get("/healthz")
    assert "Strict-Transport-Security" in r.headers
