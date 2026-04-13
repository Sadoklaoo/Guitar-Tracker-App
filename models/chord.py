from pydantic import BaseModel
from typing import Optional


class ChordResponse(BaseModel):
    id: str
    name: str
    frets: list[Optional[int]]
    fingers: Optional[list[Optional[int]]] = None
    base_fret: int = 1
    notes: Optional[str] = None
    diagram_data: Optional[str] = None

    class Config:
        populate_by_name = True
