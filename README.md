# 🎸 Guitar Tracker API

A FastAPI backend for tracking songs, chords, and fingerstyle pieces. Built with Motor (async MongoDB), Pydantic v2, and Uvicorn.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Database | MongoDB |
| Driver | Motor (async) |
| Validation | Pydantic v2 |
| Server | Uvicorn |

---

## Project Structure

```
guitar_backend/
├── main.py               # App entry point, router registration
├── database.py           # MongoDB connection and collection getters
├── utils.py              # ObjectId helpers
├── .env                  # Environment variables (you create this)
├── requirements.txt
├── models/
│   ├── song.py           # Song schema
│   ├── chord.py          # Chord schema
│   └── fingerstyle.py    # Fingerstyle song schema
└── routes/
    ├── songs.py          # /songs endpoints
    ├── chords.py         # /chords endpoints
    └── fingerstyle.py    # /fingerstyle endpoints
```

---

## Setup

### 1. Clone and enter the project

```bash
cd guitar_backend
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create your `.env` file

```bash
MONGO_URL=mongodb://localhost:27017
DB_NAME=guitar_tracker
```

> For MongoDB Atlas, replace `MONGO_URL` with your connection string:
> `MONGO_URL=mongodb+srv://<user>:<password>@cluster.mongodb.net`

### 4. Run the server

```bash
python main.py
```

Server runs at `http://localhost:8000`
Interactive docs at `http://localhost:8000/docs`

---

## API Endpoints

### Songs

| Method | Endpoint | Description |
|---|---|---|
| GET | `/songs` | List all songs |
| POST | `/songs` | Create a song |
| GET | `/songs/{id}` | Get a song |
| PUT | `/songs/{id}` | Update a song |
| DELETE | `/songs/{id}` | Delete a song |
| GET | `/songs/{id}/chords` | Get chords used in a song |

### Chords

| Method | Endpoint | Description |
|---|---|---|
| GET | `/chords` | List all chords from local JSON |
| GET | `/chords/{id}` | Get a chord from local JSON |

### Fingerstyle Songs

| Method | Endpoint | Description |
|---|---|---|
| GET | `/fingerstyle` | List all fingerstyle songs (filterable) |
| POST | `/fingerstyle` | Create a fingerstyle song |
| GET | `/fingerstyle/{id}` | Get a fingerstyle song |
| PUT | `/fingerstyle/{id}` | Update a fingerstyle song |
| DELETE | `/fingerstyle/{id}` | Delete a fingerstyle song |
| GET | `/fingerstyle/{id}/chords` | Get chords used in the piece |
| GET | `/fingerstyle/meta/techniques` | List all valid technique names |

#### Fingerstyle filter query params

```
GET /fingerstyle?technique=Classical&difficulty=Advanced&tuning=DADGAD&min_rating=4
```

---

## Data Schemas

### Song

A song can now be created with either a simple chord list, a chord sequence with repeat counts, or quick text input.

```json
{
  "title": "Blackbird",
  "artist": "The Beatles",
  "genre": "Rock",
  "difficulty": "Intermediate",
  "rating": 5,
  "chords": ["G", "Am", "Em"]
}
```

```json
{
  "title": "Blackbird",
  "artist": "The Beatles",
  "genre": "Rock",
  "difficulty": "Intermediate",
  "rating": 5,
  "chord_sequence": [
    {"name": "G", "repeats": 4},
    {"name": "Am", "repeats": 2},
    {"name": "Em", "repeats": 1}
  ]
}
```

```json
{
  "title": "Blackbird",
  "artist": "The Beatles",
  "genre": "Rock",
  "difficulty": "Intermediate",
  "rating": 5,
  "chord_text": "G*4 Am*2 Em"
}
```

`difficulty` must be one of: `Beginner`, `Intermediate`, `Advanced`

### Chord

```json
{
  "id": "G",
  "name": "G",
  "frets": [3, 2, 0, 0, 0, 3],
  "fingers": [2, 1, null, null, null, 3],
  "base_fret": 1,
  "notes": "Standard open G chord",
  "diagram_data": "e|--3--\nB|--0--\nG|--0--\nD|--0--\nA|--2--\nE|--3--"
}
```

### Fingerstyle Song

Fingerstyle songs now store a full performance sequence containing both notes and chords.

```json
{
  "title": "Clair de Lune",
  "artist": "Claude Debussy",
  "genre": "Classical",
  "difficulty": "Advanced",
  "rating": 5,
  "technique": "Classical",
  "tuning": "Standard (EADGBe)",
  "tempo_bpm": 60,
  "time_signature": "9/8",
  "key": "D flat major",
  "capo": 0,
  "tab_url": "https://example.com/tab",
  "arrangement_notes": "Focus on dynamic contrast in the middle section",
  "sequence": [
    {"type": "chord", "value": "Dbmaj7", "repeats": 4},
    {"type": "note", "value": "F4", "duration": "quarter"},
    {"type": "chord", "value": "Abmaj7", "repeats": 2}
  ]
}
```

`technique` must be one of:
`Travis Picking`, `Classical`, `Flamenco`, `Percussive`, `Hybrid Picking`, `Two-Finger`, `Three-Finger`, `Arpeggio`, `Chord-Melody`, `Other`

---

## MongoDB Collections

| Collection | Description |
|---|---|
| `songs` | Standard songs |
| `chords` | Chord library |
| `fingerstyle_songs` | Fingerstyle-specific songs |

---

## Development Notes

- All endpoints are async using Motor
- ObjectIds are serialized to strings in all responses
- Fingerstyle songs now store a full `sequence` payload for notes and chords
- `.env` is required at startup — the app will fail to connect without `MONGO_URL`
- `.env` is required at startup — the app will fail to connect without `MONGO_URL`