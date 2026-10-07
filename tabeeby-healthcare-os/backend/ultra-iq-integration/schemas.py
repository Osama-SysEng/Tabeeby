"""Schemas for ultra-iq-integration"""
from pydantic import BaseModel, Field
from typing import Optional
class Ultra_Iq_IntegrationSchema(BaseModel):
    name: str = Field(..., description="Name")
    description: Optional[str] = None
