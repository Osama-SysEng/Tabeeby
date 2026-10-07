"""Tests for edge-computing models"""
from models import Edge_ComputingCreate, Edge_ComputingResponse
def test_create():
    item = Edge_ComputingCreate(name="Test")
    assert item.name == "Test"
def test_response():
    item = Edge_ComputingResponse(id="t1", name="Test", created_at="2024-01-01T00:00:00")
    assert item.id == "t1"
