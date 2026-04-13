from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class DifficultyLevel(str, Enum):
    beginner = "Beginner"
    intermediate = "Intermediate"
    advanced = "Advanced"


class SongCreate(BaseModel):
    title: str
    artist: str
    genre: str
    difficulty: DifficultyLevel
    rating: int = Field(..., ge=1, le=5)
    chords: list[str] = []


class SongUpdate(BaseModel):
    title: Optional[str] = None
    artist: Optional[str] = None
    genre: Optional[str] = None
    difficulty: Optional[DifficultyLevel] = None
    rating: Optional[int] = Field(default=None, ge=1, le=5)
    chords: Optional[list[str]] = None


class SongResponse(BaseModel):
    id: str
    title: str
    artist: str
    genre: str
    difficulty: DifficultyLevel
    rating: int
    chords: list[str]
    created_at: datetime

    class Config:
        populate_by_name = True
