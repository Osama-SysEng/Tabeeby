"""Tests for ultra-iq-integration models"""
from models import Ultra_Iq_IntegrationCreate, Ultra_Iq_IntegrationResponse
def test_create():
    item = Ultra_Iq_IntegrationCreate(name="Test")
    assert item.name == "Test"
def test_response():
    item = Ultra_Iq_IntegrationResponse(id="t1", name="Test", created_at="2024-01-01T00:00:00")
    assert item.id == "t1"
