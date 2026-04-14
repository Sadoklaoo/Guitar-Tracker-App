from fastapi import APIRouter, HTTPException, status, Query
from bson import ObjectId
from datetime import datetime, timezone
from typing import Optional

from database import get_fingerstyle_collection
from models.fingerstyle import (
    FingerstyleSongCreate,
    FingerstyleSongUpdate,
    FingerstyleSongResponse,
    FingerstyleTechnique,
    DifficultyLevel,
)
from models.chord import ChordResponse
from utils import (
    doc_to_dict,
    get_chords_by_names,
    valid_object_id,
    derive_chords_from_fingerstyle_data,
)

router = APIRouter(prefix="/fingerstyle", tags=["Fingerstyle Songs"])


# ── List & filter ────────────────────────────────────────────────────────────

@router.get("", response_model=list[FingerstyleSongResponse])
async def list_fingerstyle_songs(
    technique: Optional[FingerstyleTechnique] = Query(default=None),
    difficulty: Optional[DifficultyLevel] = Query(default=None),
    tuning: Optional[str] = Query(default=None),
    min_rating: Optional[int] = Query(default=None, ge=1, le=5),
):
    """List fingerstyle songs with optional filters."""
    collection = get_fingerstyle_collection()
    query: dict = {}
    if technique:
        query["technique"] = technique
    if difficulty:
        query["difficulty"] = difficulty
    if tuning:
        query["tuning"] = tuning
    if min_rating is not None:
        query["rating"] = {"$gte": min_rating}

    songs = await collection.find(query).sort("created_at", -1).to_list(length=None)
    return [doc_to_dict(s) for s in songs]


# ── Create ───────────────────────────────────────────────────────────────────

@router.post("", response_model=FingerstyleSongResponse, status_code=status.HTTP_201_CREATED)
async def create_fingerstyle_song(payload: FingerstyleSongCreate):
    collection = get_fingerstyle_collection()
    doc = payload.model_dump()
    sequence = doc.get("sequence") or []
    chord_ids = doc.get("chordIds") or []
    doc["chords"] = derive_chords_from_fingerstyle_data(sequence, chord_ids)
    doc["created_at"] = datetime.now(timezone.utc)
    result = await collection.insert_one(doc)
    created = await collection.find_one({"_id": result.inserted_id})
    return doc_to_dict(created)


# ── Read one ─────────────────────────────────────────────────────────────────

@router.get("/{id}", response_model=FingerstyleSongResponse)
async def get_fingerstyle_song(id: str):
    if not valid_object_id(id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    collection = get_fingerstyle_collection()
    song = await collection.find_one({"_id": ObjectId(id)})
    if not song:
        raise HTTPException(status_code=404, detail="Fingerstyle song not found")
    return doc_to_dict(song)


# ── Update ───────────────────────────────────────────────────────────────────

@router.put("/{id}", response_model=FingerstyleSongResponse)
async def update_fingerstyle_song(id: str, payload: FingerstyleSongUpdate):
    if not valid_object_id(id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    collection = get_fingerstyle_collection()
    update_data = {k: v for k, v in payload.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    if "sequence" in update_data or "chordIds" in update_data:
        sequence = update_data.get("sequence")
        chord_ids = update_data.get("chordIds")
        computed_chords = derive_chords_from_fingerstyle_data(
            sequence or [],
            chord_ids,
        )
        update_data["chords"] = computed_chords
        if "sequence" in update_data and update_data.get("sequence") is not None:
            update_data.setdefault("chordIds", [])

    result = await collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": update_data},
        return_document=True,
    )
    if not result:
        raise HTTPException(status_code=404, detail="Fingerstyle song not found")
    return doc_to_dict(result)


# ── Delete ───────────────────────────────────────────────────────────────────

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_fingerstyle_song(id: str):
    if not valid_object_id(id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    collection = get_fingerstyle_collection()
    result = await collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Fingerstyle song not found")


# ── Chords for a fingerstyle song ────────────────────────────────────────────

@router.get("/{id}/chords", response_model=list[ChordResponse])
async def get_chords_for_fingerstyle_song(id: str):
    if not valid_object_id(id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    fs_col = get_fingerstyle_collection()

    song = await fs_col.find_one({"_id": ObjectId(id)})
    if not song:
        raise HTTPException(status_code=404, detail="Fingerstyle song not found")

    chord_names = song.get("chords", []) or []
    if not chord_names and song.get("sequence"):
        chord_names = [
            item.get("value")
            for item in song["sequence"]
            if isinstance(item, dict) and item.get("type") == "chord" and item.get("value")
        ]

    chords = get_chords_by_names(chord_names)
    return [doc_to_dict(c) for c in chords]


# ── Techniques reference ──────────────────────────────────────────────────────

@router.get("/meta/techniques", response_model=list[str])
async def list_techniques():
    """Return all supported fingerstyle technique names."""
    return [t.value for t in FingerstyleTechnique]
