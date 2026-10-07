"""Models for vr-ar-platform"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
class Vr_Ar_PlatformBase(BaseModel):
    id: Optional[str] = None
    created_at: Optional[datetime] = None
class Vr_Ar_PlatformCreate(BaseModel):
    name: str
    description: Optional[str] = None
class Vr_Ar_PlatformResponse(BaseModel):
    id: str; name: str; description: Optional[str]; created_at: datetime
