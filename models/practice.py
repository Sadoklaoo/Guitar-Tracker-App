from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PracticeCreate(BaseModel):
    duration_minutes: int
    notes: Optional[str] = None


class PracticeResponse(BaseModel):
    id: str
    song_id: str
    duration_minutes: int
    notes: Optional[str] = None
    practiced_at: datetime

    class Config:
        populate_by_name = True
