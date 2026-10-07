"""Schemas for virtual-nanobot"""
from pydantic import BaseModel, Field
from typing import Optional
class Virtual_NanobotSchema(BaseModel):
    name: str = Field(..., description="Name")
    description: Optional[str] = None
