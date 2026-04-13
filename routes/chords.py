from fastapi import APIRouter, HTTPException, status
from bson import ObjectId

from database import get_chords_collection
from models.chord import ChordCreate, ChordResponse
from utils import doc_to_dict, valid_object_id

router = APIRouter(prefix="/chords", tags=["Chords"])


@router.get("", response_model=list[ChordResponse])
async def list_chords():
    collection = get_chords_collection()
    chords = await collection.find().to_list(length=None)
    return [doc_to_dict(c) for c in chords]


@router.post("", response_model=ChordResponse, status_code=status.HTTP_201_CREATED)
async def create_chord(payload: ChordCreate):
    collection = get_chords_collection()
    doc = payload.model_dump()
    result = await collection.insert_one(doc)
    created = await collection.find_one({"_id": result.inserted_id})
    return doc_to_dict(created)


@router.get("/{id}", response_model=ChordResponse)
async def get_chord(id: str):
    if not valid_object_id(id):
        raise HTTPException(status_code=400, detail="Invalid chord ID")
    collection = get_chords_collection()
    chord = await collection.find_one({"_id": ObjectId(id)})
    if not chord:
        raise HTTPException(status_code=404, detail="Chord not found")
    return doc_to_dict(chord)
