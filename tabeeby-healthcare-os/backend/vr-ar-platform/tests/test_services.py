"""Tests for vr-ar-platform services"""
from services.core import Vr_Ar_PlatformService
def test_create():
    svc = Vr_Ar_PlatformService(db={})
    item = svc.create(name="Test")
    assert item["id"] is not None
def test_get():
    svc = Vr_Ar_PlatformService(db={"t1": {"id": "t1", "name": "Test"}})
    item = svc.get("t1")
    assert item is not None
def test_update():
    svc = Vr_Ar_PlatformService(db={"t1": {"id": "t1", "name": "Test"}})
    u = svc.update("t1", {"name": "Updated"})
    assert u["name"] == "Updated"
def test_delete():
    svc = Vr_Ar_PlatformService(db={"t1": {"id": "t1"}})
    assert svc.delete("t1") is True
    assert svc.get("t1") is None
