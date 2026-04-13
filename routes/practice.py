from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from datetime import datetime, timezone

from database import get_practice_collection, get_songs_collection
from models.practice import PracticeCreate, PracticeResponse
from utils import doc_to_dict, valid_object_id

router = APIRouter(tags=["Practice Sessions"])


@router.post("/songs/{id}/practice", response_model=PracticeResponse, status_code=status.HTTP_201_CREATED)
async def log_practice_session(id: str, payload: PracticeCreate):
    if not valid_object_id(id):
        raise HTTPException(status_code=400, detail="Invalid song ID")

    songs_col = get_songs_collection()
    song = await songs_col.find_one({"_id": ObjectId(id)})
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")

    practice_col = get_practice_collection()
    doc = payload.model_dump()
    doc["song_id"] = id
    doc["practiced_at"] = datetime.now(timezone.utc)
    result = await practice_col.insert_one(doc)
    created = await practice_col.find_one({"_id": result.inserted_id})
    return doc_to_dict(created)


@router.get("/songs/{id}/practice", response_model=list[PracticeResponse])
async def get_practice_history(id: str):
    if not valid_object_id(id):
        raise HTTPException(status_code=400, detail="Invalid song ID")

    songs_col = get_songs_collection()
    song = await songs_col.find_one({"_id": ObjectId(id)})
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")

    practice_col = get_practice_collection()
    sessions = await practice_col.find({"song_id": id}).sort("practiced_at", -1).to_list(length=None)
    return [doc_to_dict(s) for s in sessions]
