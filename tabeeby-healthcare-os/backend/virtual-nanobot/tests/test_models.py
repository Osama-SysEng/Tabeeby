"""Tests for virtual-nanobot models"""
from models import Virtual_NanobotCreate, Virtual_NanobotResponse
def test_create():
    item = Virtual_NanobotCreate(name="Test")
    assert item.name == "Test"
def test_response():
    item = Virtual_NanobotResponse(id="t1", name="Test", created_at="2024-01-01T00:00:00")
    assert item.id == "t1"
