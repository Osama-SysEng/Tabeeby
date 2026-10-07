"""Tests for drug-discovery services"""
from services.core import Drug_DiscoveryService
def test_create():
    svc = Drug_DiscoveryService(db={})
    item = svc.create(name="Test")
    assert item["id"] is not None
def test_get():
    svc = Drug_DiscoveryService(db={"t1": {"id": "t1", "name": "Test"}})
    item = svc.get("t1")
    assert item is not None
def test_update():
    svc = Drug_DiscoveryService(db={"t1": {"id": "t1", "name": "Test"}})
    u = svc.update("t1", {"name": "Updated"})
    assert u["name"] == "Updated"
def test_delete():
    svc = Drug_DiscoveryService(db={"t1": {"id": "t1"}})
    assert svc.delete("t1") is True
    assert svc.get("t1") is None
