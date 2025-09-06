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
    return TestClient(get_app())


def test_metrics_labels(monkeypatch):
    c = create_client(monkeypatch)
    c.get("/healthz")
    c.post("/v1/assess", json=CLAIM)
    c.post("/v1/assess", json=CLAIM)
    metrics = c.get("/metrics").text
    assert 'codexia_requests_total{method="GET",path="/healthz",status="200"}' in metrics
    assert 'codexia_requests_total{method="POST",path="/v1/assess",status="200"}' in metrics
    assert 'codexia_request_latency_seconds_bucket{le="0.01",method="POST",path="/v1/assess"}' in metrics
