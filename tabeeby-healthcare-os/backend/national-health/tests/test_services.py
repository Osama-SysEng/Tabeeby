"""Tests for national-health services"""
from services.core import National_HealthService
def test_create():
    svc = National_HealthService(db={})
    item = svc.create(name="Test")
    assert item["id"] is not None
def test_get():
    svc = National_HealthService(db={"t1": {"id": "t1", "name": "Test"}})
    item = svc.get("t1")
    assert item is not None
def test_update():
    svc = National_HealthService(db={"t1": {"id": "t1", "name": "Test"}})
    u = svc.update("t1", {"name": "Updated"})
    assert u["name"] == "Updated"
def test_delete():
    svc = National_HealthService(db={"t1": {"id": "t1"}})
    assert svc.delete("t1") is True
