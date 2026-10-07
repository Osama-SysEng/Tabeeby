"""Tests for edge-computing services"""
from services.core import Edge_ComputingService
def test_create():
    svc = Edge_ComputingService(db={})
    item = svc.create(name="Test")
    assert item["id"] is not None
def test_get():
    svc = Edge_ComputingService(db={"t1": {"id": "t1", "name": "Test"}})
    item = svc.get("t1")
    assert item is not None
def test_update():
    svc = Edge_ComputingService(db={"t1": {"id": "t1", "name": "Test"}})
    u = svc.update("t1", {"name": "Updated"})
    assert u["name"] == "Updated"
def test_delete():
    svc = Edge_ComputingService(db={"t1": {"id": "t1"}})
    assert svc.delete("t1") is True
    assert svc.get("t1") is None
