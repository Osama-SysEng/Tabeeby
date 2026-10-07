"""Models for drug-discovery"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
class Drug_DiscoveryBase(BaseModel):
    id: Optional[str] = None
    created_at: Optional[datetime] = None
class Drug_DiscoveryCreate(BaseModel):
    name: str
    description: Optional[str] = None
class Drug_DiscoveryResponse(BaseModel):
    id: str; name: str; description: Optional[str]; created_at: datetime
