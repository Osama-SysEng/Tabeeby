"""Tests for ai-physician models"""
from models import Ai_PhysicianCreate, Ai_PhysicianResponse
def test_create():
    item = Ai_PhysicianCreate(name="Test")
    assert item.name == "Test"
def test_response():
    item = Ai_PhysicianResponse(id="t1", name="Test", created_at="2024-01-01T00:00:00")
    assert item.id == "t1"
