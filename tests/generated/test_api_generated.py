"""
Auto-generated API tests
"""
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get__api_components_search():
    resp = client.get("/api/components/search")
    assert resp.status_code < 500


def test_get__api_components_id():
    resp = client.get("/api/components/R1")
    assert resp.status_code < 500


def test_post__api_designs():
    resp = client.post("/api/designs")
    assert resp.status_code < 500
