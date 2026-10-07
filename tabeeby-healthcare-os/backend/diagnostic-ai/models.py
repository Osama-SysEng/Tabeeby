"""Models for diagnostic-ai"""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
class Diagnostic_AiBase(BaseModel):
    id: Optional[str] = None
    created_at: Optional[datetime] = None
class Diagnostic_AiCreate(BaseModel):
    name: str
    description: Optional[str] = None
class Diagnostic_AiResponse(BaseModel):
    id: str; name: str; description: Optional[str]; created_at: datetime
