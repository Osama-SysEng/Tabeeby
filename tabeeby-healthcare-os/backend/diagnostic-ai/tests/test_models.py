"""Tests for diagnostic-ai models"""
from models import Diagnostic_AiCreate, Diagnostic_AiResponse
def test_create():
    item = Diagnostic_AiCreate(name="Test")
    assert item.name == "Test"
def test_response():
    item = Diagnostic_AiResponse(id="t1", name="Test", created_at="2024-01-01T00:00:00")
    assert item.id == "t1"
