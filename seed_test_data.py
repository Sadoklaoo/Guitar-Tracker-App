import asyncio
from datetime import datetime, timezone

from database import connect_db, close_db, get_songs_collection, get_fingerstyle_collection


TEST_SONGS = [
    {
        "title": "Blackbird",
        "artist": "The Beatles",
        "genre": "Folk Rock",
        "difficulty": "Intermediate",
        "rating": 5,
        "chord_text": "G*4 D*2 Em C",
    },
    {
        "title": "Wonderwall",
        "artist": "Oasis",
        "genre": "Britpop",
        "difficulty": "Beginner",
        "rating": 4,
        "chord_sequence": [
            {"name": "Em7", "repeats": 4},
            {"name": "G", "repeats": 2},
            {"name": "Dsus4", "repeats": 2},
            {"name": "A7sus4", "repeats": 4},
        ],
    },
    {
        "title": "Hotel California",
        "artist": "Eagles",
        "genre": "Rock",
        "difficulty": "Advanced",
        "rating": 5,
        "chords": ["Bm", "F#", "A", "E", "G", "D", "Em"],
    },
]

TEST_FINGERSTYLE_SONGS = [
    {
        "title": "Classical Breeze",
        "artist": "Test Artist",
        "genre": "Classical",
        "difficulty": "Advanced",
        "rating": 5,
        "technique": "Classical",
        "tuning": "Standard",
        "tempo_bpm": 70,
        "time_signature": "6/8",
        "key": "D minor",
        "capo": 0,
        "tab_url": "https://example.com/classical-breeze",
        "arrangement_notes": "Gentle arpeggios with melodic chord accents.",
        "sequence": [
            {"type": "chord", "value": "Dm", "duration": 2.0},
            {"type": "note", "value": "F4", "duration": 0.5},
            {"type": "note", "value": "A4", "duration": 0.5},
            {"type": "chord", "value": "Bb", "duration": 2.0},
            {"type": "note", "value": "G4", "duration": 0.5},
            {"type": "chord", "value": "C", "duration": 2.0},
        ],
    },
    {
        "title": "Morning Walk",
        "artist": "Test Artist",
        "genre": "Acoustic",
        "difficulty": "Intermediate",
        "rating": 4,
        "technique": "Travis Picking",
        "tuning": "DADGAD",
        "tempo_bpm": 90,
        "time_signature": "4/4",
        "key": "G major",
        "capo": 2,
        "tab_url": "https://example.com/morning-walk",
        "arrangement_notes": "Open tuning arpeggio with melodic bass movement.",
        "sequence": [
            {"type": "chord", "value": "G", "duration": 3.0},
            {"type": "note", "value": "B3", "duration": 0.25},
            {"type": "chord", "value": "Cadd9", "duration": 3.0},
            {"type": "note", "value": "D4", "duration": 0.25},
        ],
    },
    {
        "title": "Legacy Chord Flow",
        "artist": "Test Artist",
        "genre": "Folk",
        "difficulty": "Beginner",
        "rating": 3,
        "technique": "Travis Picking",
        "tuning": "Standard",
        "tempo_bpm": 80,
        "time_signature": "4/4",
        "key": "C major",
        "capo": 0,
        "tab_url": "https://example.com/legacy-chord-flow",
        "arrangement_notes": "Legacy song using chordIds fallback.",
        "sequence": [],
        "chordIds": ["Am", "C", "G", "F"],
    },
]


async def seed_data() -> None:
    await connect_db()
    try:
        songs_collection = get_songs_collection()
        fingerstyle_collection = get_fingerstyle_collection()

        print("Clearing existing songs...")
        await songs_collection.delete_many({})
        await fingerstyle_collection.delete_many({})

        timestamp = datetime.now(timezone.utc)

        song_docs = [
            {**song, "created_at": timestamp}
            for song in TEST_SONGS
        ]
        fingerstyle_docs = [
            {**song, "created_at": timestamp}
            for song in TEST_FINGERSTYLE_SONGS
        ]

        if song_docs:
            result = await songs_collection.insert_many(song_docs)
            print(f"Inserted {len(result.inserted_ids)} test songs.")

        if fingerstyle_docs:
            result = await fingerstyle_collection.insert_many(fingerstyle_docs)
            print(f"Inserted {len(result.inserted_ids)} test fingerstyle songs.")

        print("Seed complete.")
    finally:
        await close_db()


if __name__ == "__main__":
    asyncio.run(seed_data())
