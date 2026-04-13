from fastapi import APIRouter, HTTPException

from models.chord import ChordResponse
from utils import get_all_chords, get_chord_by_name_or_id

router = APIRouter(prefix="/chords", tags=["Chords"])


@router.get("", response_model=list[ChordResponse])
async def list_chords():
    return get_all_chords()


@router.get("/{id}", response_model=ChordResponse)
async def get_chord(id: str):
    chord = get_chord_by_name_or_id(id)
    if not chord:
        raise HTTPException(status_code=404, detail="Chord not found")
    return chord
