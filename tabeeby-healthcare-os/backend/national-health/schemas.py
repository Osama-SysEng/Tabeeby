"""Schemas for national-health"""
from pydantic import BaseModel, Field
from typing import Optional
class National_HealthSchema(BaseModel):
    name: str = Field(..., description="Name")
    description: Optional[str] = None
