"""Models for ultra-iq-integration"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
class Ultra_Iq_IntegrationBase(BaseModel):
    id: Optional[str] = None
    created_at: Optional[datetime] = None
class Ultra_Iq_IntegrationCreate(BaseModel):
    name: str
    description: Optional[str] = None
class Ultra_Iq_IntegrationResponse(BaseModel):
    id: str; name: str; description: Optional[str]; created_at: datetime
