"""Models for ai-physician"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
class Ai_PhysicianBase(BaseModel):
    id: Optional[str] = None
    created_at: Optional[datetime] = None
class Ai_PhysicianCreate(BaseModel):
    name: str
    description: Optional[str] = None
class Ai_PhysicianResponse(BaseModel):
    id: str; name: str; description: Optional[str]; created_at: datetime
