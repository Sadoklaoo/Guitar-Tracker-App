# 🎸 Guitar Tracker API

A FastAPI backend for tracking songs, chords, fingerstyle pieces, and practice sessions. Built with Motor (async MongoDB), Pydantic v2, and Uvicorn.

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
│   ├── practice.py       # Practice session schema
│   └── fingerstyle.py    # Fingerstyle song schema
└── routes/
    ├── songs.py          # /songs endpoints
    ├── chords.py         # /chords endpoints
    ├── practice.py       # /songs/{id}/practice endpoints
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
| POST | `/songs/{id}/practice` | Log a practice session |
| GET | `/songs/{id}/practice` | Get practice history |

### Chords

| Method | Endpoint | Description |
|---|---|---|
| GET | `/chords` | List all chords |
| POST | `/chords` | Create a chord |
| GET | `/chords/{id}` | Get a chord |

### Fingerstyle Songs

| Method | Endpoint | Description |
|---|---|---|
| GET | `/fingerstyle` | List all fingerstyle songs (filterable) |
| POST | `/fingerstyle` | Create a fingerstyle song |
| GET | `/fingerstyle/{id}` | Get a fingerstyle song |
| PUT | `/fingerstyle/{id}` | Update a fingerstyle song |
| DELETE | `/fingerstyle/{id}` | Delete a fingerstyle song |
| GET | `/fingerstyle/{id}/chords` | Get chords used in the piece |
| POST | `/fingerstyle/{id}/practice` | Log a practice session |
| GET | `/fingerstyle/{id}/practice` | Get practice history |
| GET | `/fingerstyle/meta/techniques` | List all valid technique names |

#### Fingerstyle filter query params

```
GET /fingerstyle?technique=Classical&difficulty=Advanced&tuning=DADGAD&min_rating=4
```

---

## Data Schemas

### Song

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

`difficulty` must be one of: `Beginner`, `Intermediate`, `Advanced`

### Chord

```json
{
  "name": "Em7",
  "finger_positions": [
    { "string": 2, "fret": 2, "finger": 2 },
    { "string": 3, "fret": 2, "finger": 3 }
  ],
  "diagram_data": null
}
```

### Practice Session

```json
{
  "duration_minutes": 30,
  "notes": "Worked on the bridge section"
}
```

### Fingerstyle Song

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
  "chords": ["Dbmaj7", "Abmaj7"]
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
| `practice_sessions` | Practice logs for both song types |
| `fingerstyle_songs` | Fingerstyle-specific songs |

---

## Development Notes

- All endpoints are async using Motor
- ObjectIds are serialized to strings in all responses
- Fingerstyle practice sessions are tagged with `song_type: "fingerstyle"` in the `practice_sessions` collection to distinguish them from regular song sessions
- `.env` is required at startup — the app will fail to connect without `MONGO_URL`