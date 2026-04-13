from pydantic import BaseModel, Field
from typing import Optional
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


class FingerstyleSongCreate(BaseModel):
    title: str
    artist: str
    genre: str
    difficulty: DifficultyLevel
    rating: int = Field(..., ge=1, le=5)

    # Fingerstyle-specific fields
    technique: FingerstyleTechnique
    tuning: str = Field(default="Standard (EADGBe)", description="Guitar tuning, e.g. DADGAD, Drop D")
    tempo_bpm: Optional[int] = Field(default=None, ge=20, le=300, description="Approximate BPM")
    time_signature: str = Field(default="4/4", description="Time signature, e.g. 3/4, 6/8")
    key: Optional[str] = Field(default=None, description="Key of the piece, e.g. G major, A minor")
    capo: Optional[int] = Field(default=None, ge=0, le=12, description="Capo position (0 = no capo)")
    tab_url: Optional[str] = Field(default=None, description="Link to tab or sheet music")
    arrangement_notes: Optional[str] = Field(default=None, description="Notes on the arrangement style")
    chords: list[str] = []


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
    chords: Optional[list[str]] = None


class FingerstyleSongResponse(BaseModel):
    id: str
    title: str
    artist: str
    genre: str
    difficulty: DifficultyLevel
    rating: int
    technique: FingerstyleTechnique
    tuning: str
    tempo_bpm: Optional[int] = None
    time_signature: str
    key: Optional[str] = None
    capo: Optional[int] = None
    tab_url: Optional[str] = None
    arrangement_notes: Optional[str] = None
    chords: list[str]
    created_at: datetime

    class Config:
        populate_by_name = True
