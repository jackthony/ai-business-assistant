from fastapi.testclient import TestClient

from src.api.main import app


def test_health_ok():
    client = TestClient(app)
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_health_method_not_allowed():
    client = TestClient(app)
    assert client.post("/health").status_code == 405
