import pytest
from fastapi.testclient import TestClient
import pathlib
import sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "backend" / "api-gateway"))
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_services_status():
    response = client.get("/api/v1/services/status")
    assert response.status_code == 200
    assert "ultra-iq" in response.json()
