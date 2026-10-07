"""Schemas for ai-physician"""
from pydantic import BaseModel, Field
from typing import Optional
class Ai_PhysicianSchema(BaseModel):
    name: str = Field(..., description="Name")
    description: Optional[str] = None
