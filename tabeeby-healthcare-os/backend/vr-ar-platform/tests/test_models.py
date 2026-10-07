"""Tests for vr-ar-platform models"""
from models import Vr_Ar_PlatformCreate, Vr_Ar_PlatformResponse
def test_create():
    item = Vr_Ar_PlatformCreate(name="Test")
    assert item.name == "Test"
def test_response():
    item = Vr_Ar_PlatformResponse(id="t1", name="Test", created_at="2024-01-01T00:00:00")
    assert item.id == "t1"
