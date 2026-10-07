"""Models for edge-computing"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
class Edge_ComputingBase(BaseModel):
    id: Optional[str] = None
    created_at: Optional[datetime] = None
class Edge_ComputingCreate(BaseModel):
    name: str
    description: Optional[str] = None
class Edge_ComputingResponse(BaseModel):
    id: str; name: str; description: Optional[str]; created_at: datetime
