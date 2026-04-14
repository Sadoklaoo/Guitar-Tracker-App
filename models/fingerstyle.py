from pydantic import BaseModel, Field
from typing import Optional, Literal, List
from datetime import datetime
from enum import Enum


class FingerstyleTechnique(str, Enum):
    travis_picking = "Travis Picking"
    classical = "Classical"
    flamenco = "Flamenco"
    percussive = "Percussive"
    hybrid_picking = "Hybrid Picking"
    two_finger = "Two-Finger"
    three_finger = "Three-Finger"
    arpeggio = "Arpeggio"
    chord_melody = "Chord-Melody"
    other = "Other"


class DifficultyLevel(str, Enum):
    beginner = "Beginner"
    intermediate = "Intermediate"
    advanced = "Advanced"


class SequenceItem(BaseModel):
    type: Literal["note", "chord"]
    value: str
    duration: float


class FingerstyleSongCreate(BaseModel):
    title: str
    artist: str
    genre: Optional[str] = None
    difficulty: Optional[DifficultyLevel] = None
    rating: Optional[int] = Field(default=None, ge=1, le=5)
    technique: Optional[FingerstyleTechnique] = None
    tuning: Optional[str] = None
    tempo_bpm: Optional[int] = Field(default=None, ge=20, le=300)
    time_signature: Optional[str] = None
    key: Optional[str] = None
    capo: Optional[int] = Field(default=None, ge=0, le=12)
    tab_url: Optional[str] = None
    arrangement_notes: Optional[str] = None
    sequence: Optional[List[SequenceItem]] = Field(default_factory=list)
    chordIds: Optional[List[str]] = Field(default_factory=list)


class FingerstyleSongUpdate(BaseModel):
    title: Optional[str] = None
    artist: Optional[str] = None
    genre: Optional[str] = None
    difficulty: Optional[DifficultyLevel] = None
    rating: Optional[int] = Field(default=None, ge=1, le=5)
    technique: Optional[FingerstyleTechnique] = None
    tuning: Optional[str] = None
    tempo_bpm: Optional[int] = Field(default=None, ge=20, le=300)
    time_signature: Optional[str] = None
    key: Optional[str] = None
    capo: Optional[int] = Field(default=None, ge=0, le=12)
    tab_url: Optional[str] = None
    arrangement_notes: Optional[str] = None
    sequence: Optional[List[SequenceItem]] = None
    chordIds: Optional[List[str]] = None


class FingerstyleSongResponse(BaseModel):
    id: str
    title: str
    artist: str
    genre: Optional[str] = None
    difficulty: Optional[DifficultyLevel] = None
    rating: Optional[int] = None
    technique: Optional[FingerstyleTechnique] = None
    tuning: Optional[str] = None
    tempo_bpm: Optional[int] = None
    time_signature: Optional[str] = None
    key: Optional[str] = None
    capo: Optional[int] = None
    tab_url: Optional[str] = None
    arrangement_notes: Optional[str] = None
    sequence: List[SequenceItem] = Field(default_factory=list)
    chordIds: List[str] = Field(default_factory=list)
    created_at: datetime

    class Config:
        populate_by_name = True
