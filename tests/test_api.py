import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data

def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_create_design():
    """Test circuit design creation"""
    payload = {
        "description": "Design a simple RC filter",
        "constraints": {"frequency": "1kHz"}
    }
    response = client.post("/api/v1/designs", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "design_id" in data
    assert data["status"] == "processing"

def test_create_design_invalid():
    """Test design creation with invalid data"""
    response = client.post("/api/v1/designs", json={})
    assert response.status_code == 422  # Validation error
