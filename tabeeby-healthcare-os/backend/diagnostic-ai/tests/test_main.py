"""Tests for diagnostic-ai"""
from fastapi.testclient import TestClient
from main import app
client = TestClient(app)
def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
def test_create():
    r = client.post("/start", json={"name": "Test"})
    assert r.status_code == 200
    assert "id" in r.json()
def test_list():
    r = client.get("/list")
    assert r.status_code == 200
def test_get():
    cr = client.post("/start", json={"name": "Test"})
    iid = cr.json()["id"]
    r = client.get(f"/list/{iid}")
    assert r.status_code == 200
def test_update():
    cr = client.post("/start", json={"name": "Test"})
    iid = cr.json()["id"]
    r = client.put(f"/list/{iid}/update", json={"description": "Updated"})
    assert r.status_code == 200
def test_delete():
    cr = client.post("/start", json={"name": "Test"})
    iid = cr.json()["id"]
    r = client.delete(f"/list/{iid}")
    assert r.status_code == 200
