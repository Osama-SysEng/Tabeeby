"""Schemas for surgical-suite"""
from pydantic import BaseModel, Field
from typing import Optional
class Surgical_SuiteSchema(BaseModel):
    name: str = Field(..., description="Name")
    description: Optional[str] = None
