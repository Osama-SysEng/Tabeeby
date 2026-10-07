"""Models for national-health"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
class National_HealthBase(BaseModel):
    id: Optional[str] = None
    created_at: Optional[datetime] = None
class National_HealthCreate(BaseModel):
    name: str
    description: Optional[str] = None
class National_HealthResponse(BaseModel):
    id: str; name: str; description: Optional[str]; created_at: datetime
