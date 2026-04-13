from bson import ObjectId
from datetime import datetime


def doc_to_dict(doc: dict) -> dict:
    """Convert a MongoDB document to a JSON-serializable dict."""
    if doc is None:
        return None
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