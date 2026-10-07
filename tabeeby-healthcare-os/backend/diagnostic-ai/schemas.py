"""Schemas for diagnostic-ai"""
from pydantic import BaseModel, Field
from typing import Optional
class Diagnostic_AiSchema(BaseModel):
    name: str = Field(..., description="Name")
    description: Optional[str] = None
