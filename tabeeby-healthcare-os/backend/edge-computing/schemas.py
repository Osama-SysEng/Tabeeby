"""Schemas for edge-computing"""
from pydantic import BaseModel, Field
from typing import Optional
class Edge_ComputingSchema(BaseModel):
    name: str = Field(..., description="Name")
    description: Optional[str] = None
