"""Tests for surgical-suite models"""
from models import Surgical_SuiteCreate, Surgical_SuiteResponse
def test_create():
    item = Surgical_SuiteCreate(name="Test")
    assert item.name == "Test"
def test_response():
    item = Surgical_SuiteResponse(id="t1", name="Test", created_at="2024-01-01T00:00:00")
    assert item.id == "t1"
