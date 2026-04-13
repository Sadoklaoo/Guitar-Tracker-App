from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import traceback

from database import connect_db, close_db
from routes.songs import router as songs_router
from routes.chords import router as chords_router
from routes.practice import router as practice_router
from routes.fingerstyle import router as fingerstyle_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await close_db()


app = FastAPI(
    title="Guitar Tracker API",
    description="Track songs, chords, fingerstyle pieces, and practice sessions.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.middleware("http")
async def catch_exceptions(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"detail": str(e)})


app.include_router(songs_router)
app.include_router(chords_router)
app.include_router(practice_router)
app.include_router(fingerstyle_router)


@app.get("/", tags=["Health"])
async def root():
    return {"status": "ok", "message": "Guitar Tracker API is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)