"""Tests for surgical-suite services"""
from services.core import Surgical_SuiteService
def test_create():
    svc = Surgical_SuiteService(db={})
    item = svc.create(name="Test")
    assert item["id"] is not None
def test_get():
    svc = Surgical_SuiteService(db={"t1": {"id": "t1", "name": "Test"}})
    item = svc.get("t1")
    assert item is not None
def test_update():
    svc = Surgical_SuiteService(db={"t1": {"id": "t1", "name": "Test"}})
    u = svc.update("t1", {"name": "Updated"})
    assert u["name"] == "Updated"
def test_delete():
    svc = Surgical_SuiteService(db={"t1": {"id": "t1"}})
    assert svc.delete("t1") is True
