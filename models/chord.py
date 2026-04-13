from pydantic import BaseModel
from typing import Optional


class FingerPosition(BaseModel):
    string: int       # Guitar string number (1–6)
    fret: int         # Fret number (0 = open)
    finger: int       # Finger number (0 = open/muted, 1–4)


class ChordCreate(BaseModel):
    name: str
    finger_positions: list[FingerPosition] = []
    diagram_data: Optional[str] = None   # base64 image or SVG string


class ChordResponse(BaseModel):
    id: str
    name: str
    finger_positions: list[FingerPosition]
    diagram_data: Optional[str] = None

    class Config:
        populate_by_name = True
