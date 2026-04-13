from fastapi import APIRouter, HTTPException, status
from bson import ObjectId
from datetime import datetime, timezone

from database import get_songs_collection
from models.song import SongCreate, SongUpdate, SongResponse
from models.chord import ChordResponse
from utils import doc_to_dict, get_chords_by_names, valid_object_id

router = APIRouter(prefix="/songs", tags=["Songs"])


@router.get("", response_model=list[SongResponse])
async def list_songs():
    collection = get_songs_collection()
    songs = await collection.find().to_list(length=None)
    return [doc_to_dict(s) for s in songs]


@router.post("", response_model=SongResponse, status_code=status.HTTP_201_CREATED)
async def create_song(payload: SongCreate):
    collection = get_songs_collection()
    doc = payload.model_dump()
    doc["created_at"] = datetime.now(timezone.utc)
    result = await collection.insert_one(doc)
    created = await collection.find_one({"_id": result.inserted_id})
    return doc_to_dict(created)


@router.get("/{id}", response_model=SongResponse)
async def get_song(id: str):
    if not valid_object_id(id):
        raise HTTPException(status_code=400, detail="Invalid song ID")
    collection = get_songs_collection()
    song = await collection.find_one({"_id": ObjectId(id)})
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    return doc_to_dict(song)


@router.put("/{id}", response_model=SongResponse)
async def update_song(id: str, payload: SongUpdate):
    if not valid_object_id(id):
        raise HTTPException(status_code=400, detail="Invalid song ID")
    collection = get_songs_collection()
    update_data = {k: v for k, v in payload.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    result = await collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": update_data},
        return_document=True,
    )
    if not result:
        raise HTTPException(status_code=404, detail="Song not found")
    return doc_to_dict(result)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_song(id: str):
    if not valid_object_id(id):
        raise HTTPException(status_code=400, detail="Invalid song ID")
    collection = get_songs_collection()
    result = await collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Song not found")


@router.get("/{id}/chords", response_model=list[ChordResponse])
async def get_chords_for_song(id: str):
    if not valid_object_id(id):
        raise HTTPException(status_code=400, detail="Invalid song ID")
    songs_col = get_songs_collection()

    song = await songs_col.find_one({"_id": ObjectId(id)})
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")

    chord_names = song.get("chords", [])
    chords = get_chords_by_names(chord_names)
    return [doc_to_dict(c) for c in chords]
