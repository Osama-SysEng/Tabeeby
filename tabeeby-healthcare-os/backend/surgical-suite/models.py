"""Models for surgical-suite"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
class Surgical_SuiteBase(BaseModel):
    id: Optional[str] = None
    created_at: Optional[datetime] = None
class Surgical_SuiteCreate(BaseModel):
    name: str
    description: Optional[str] = None
class Surgical_SuiteResponse(BaseModel):
    id: str; name: str; description: Optional[str]; created_at: datetime
