"""Tests for ai-physician services"""
from services.core import Ai_PhysicianService
def test_create():
    svc = Ai_PhysicianService(db={})
    item = svc.create(name="Test")
    assert item["id"] is not None
def test_get():
    svc = Ai_PhysicianService(db={"t1": {"id": "t1", "name": "Test"}})
    item = svc.get("t1")
    assert item is not None
def test_update():
    svc = Ai_PhysicianService(db={"t1": {"id": "t1", "name": "Test"}})
    u = svc.update("t1", {"name": "Updated"})
    assert u["name"] == "Updated"
def test_delete():
    svc = Ai_PhysicianService(db={"t1": {"id": "t1"}})
    assert svc.delete("t1") is True
    assert svc.get("t1") is None
