from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime
from enum import Enum

from models.chord import ChordResponse


class DifficultyLevel(str, Enum):
    beginner = "Beginner"
    intermediate = "Intermediate"
    advanced = "Advanced"


class SongChordSegment(BaseModel):
    name: str
    repeats: int = Field(default=1, ge=1)


class SongCreate(BaseModel):
    title: str
    artist: str
    genre: str
    difficulty: DifficultyLevel
    rating: int = Field(..., ge=1, le=5)
    chords: list[str] = Field(default_factory=list)
    chord_sequence: list[SongChordSegment] = Field(default_factory=list)
    chord_text: Optional[str] = None


class SongUpdate(BaseModel):
    title: Optional[str] = None
    artist: Optional[str] = None
    genre: Optional[str] = None
    difficulty: Optional[DifficultyLevel] = None
    rating: Optional[int] = Field(default=None, ge=1, le=5)
    chords: Optional[list[str]] = None
    chord_sequence: Optional[list[SongChordSegment]] = None
    chord_text: Optional[str] = None


class SongResponse(BaseModel):
    id: str
    title: str
    artist: str
    genre: str
    difficulty: DifficultyLevel
    rating: int
    chords: list[str] = Field(default_factory=list)
    chord_sequence: Optional[list[SongChordSegment]] = None
    created_at: datetime

    class Config:
        populate_by_name = True
