"""Tests for national-health models"""
from models import National_HealthCreate, National_HealthResponse
def test_create():
    item = National_HealthCreate(name="Test")
    assert item.name == "Test"
def test_response():
    item = National_HealthResponse(id="t1", name="Test", created_at="2024-01-01T00:00:00")
    assert item.id == "t1"
