"""Models for virtual-nanobot"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
class Virtual_NanobotBase(BaseModel):
    id: Optional[str] = None
    created_at: Optional[datetime] = None
class Virtual_NanobotCreate(BaseModel):
    name: str
    description: Optional[str] = None
class Virtual_NanobotResponse(BaseModel):
    id: str; name: str; description: Optional[str]; created_at: datetime
