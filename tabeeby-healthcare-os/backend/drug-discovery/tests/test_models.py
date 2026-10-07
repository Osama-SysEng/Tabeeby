"""Tests for drug-discovery models"""
from models import Drug_DiscoveryCreate, Drug_DiscoveryResponse
def test_create():
    item = Drug_DiscoveryCreate(name="Test")
    assert item.name == "Test"
def test_response():
    item = Drug_DiscoveryResponse(id="t1", name="Test", created_at="2024-01-01T00:00:00")
    assert item.id == "t1"
