"""Schemas for vr-ar-platform"""
from pydantic import BaseModel, Field
from typing import Optional
class Vr_Ar_PlatformSchema(BaseModel):
    name: str = Field(..., description="Name")
    description: Optional[str] = None
