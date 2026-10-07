"""Schemas for drug-discovery"""
from pydantic import BaseModel, Field
from typing import Optional
class Drug_DiscoverySchema(BaseModel):
    name: str = Field(..., description="Name")
    description: Optional[str] = None
