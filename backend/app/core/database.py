from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import certifi
import os

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME")

client = None
db = None

async def connect_db():
    global client, db
    client = AsyncIOMotorClient(
        MONGODB_URI,
        tlsCAFile=certifi.where()
    )
    db = client[DB_NAME]
    print("✅ Connected to MongoDB!")

async def close_db():
    global client
    if client:
        client.close()
        print("🔌 MongoDB connection closed.")

def get_db():
    return db