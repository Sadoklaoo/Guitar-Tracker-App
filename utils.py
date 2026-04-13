import json
from bson import ObjectId
from datetime import datetime
from functools import lru_cache
from pathlib import Path


def doc_to_dict(doc: dict) -> dict:
    """Convert a MongoDB document to a JSON-serializable dict."""
    if doc is None:
        return None

    if "_id" in doc:
        doc["id"] = str(doc.pop("_id"))

    # Convert any remaining ObjectId or datetime values
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            doc[key] = str(value)
        elif isinstance(value, datetime):
            doc[key] = value.isoformat()
        elif isinstance(value, list):
            doc[key] = [
                str(v) if isinstance(v, ObjectId) else v
                for v in value
            ]

    return doc


def valid_object_id(id: str) -> bool:
    try:
        ObjectId(id)
        return True
    except Exception:
        return False


def _format_chord_diagram(frets: list[Optional[int]]) -> str:
    string_names = ["E", "A", "D", "G", "B", "e"]
    lines = []
    for string_name, fret in zip(string_names, frets):
        marker = "x" if fret is None else str(fret)
        lines.append(f"{string_name}|--{marker}--")
    return "\n".join(lines)


def _normalize_chord(chord: dict) -> dict:
    chord = dict(chord)

    if "frets" not in chord or not isinstance(chord.get("frets"), list) or len(chord["frets"]) != 6:
        frets = [None] * 6
        fingers = [None] * 6

        for pos in chord.get("finger_positions", []):
            string_num = pos.get("string")
            if isinstance(string_num, int) and 1 <= string_num <= 6:
                index = 6 - string_num
                frets[index] = pos.get("fret")
                fingers[index] = pos.get("finger")

        chord["frets"] = frets
        chord["fingers"] = fingers
    else:
        chord.setdefault("fingers", None)

    chord.setdefault("base_fret", 1)
    chord.setdefault("notes", None)

    if chord.get("diagram_data") is None:
        chord["diagram_data"] = _format_chord_diagram(chord["frets"])

    return chord


@lru_cache(maxsize=1)
def load_chord_definitions() -> list[dict]:
    file_path = Path(__file__).resolve().parent / "chords.json"
    with file_path.open("r", encoding="utf-8") as f:
        raw_chords = json.load(f)

    return [_normalize_chord(chord) for chord in raw_chords]


def get_all_chords() -> list[dict]:
    return load_chord_definitions()


def get_chord_by_name_or_id(identifier: str) -> dict | None:
    key = identifier.lower()
    for chord in load_chord_definitions():
        if chord.get("name", "").lower() == key or chord.get("id", "").lower() == key:
            return chord
    return None


def get_chords_by_names(names: list[str]) -> list[dict]:
    if not names:
        return []

    chord_map = {chord.get("name", "").lower(): chord for chord in load_chord_definitions()}
    return [chord_map[name.lower()] for name in names if name and name.lower() in chord_map]