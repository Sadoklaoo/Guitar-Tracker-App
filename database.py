import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "guitar_tracker")

client: AsyncIOMotorClient = None


async def connect_db():
    global client
    client = AsyncIOMotorClient(MONGO_URL)
    print(f"Connected to MongoDB at {MONGO_URL}")


async def close_db():
    global client
    if client:
        client.close()
        print("MongoDB connection closed")


def get_database():
    return client[DB_NAME]


def get_songs_collection():
    return get_database()["songs"]


def get_fingerstyle_collection():
    return get_database()["fingerstyle_songs"]
