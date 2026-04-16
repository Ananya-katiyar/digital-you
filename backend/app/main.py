from fastapi import FastAPI
from app.core.database import connect_db, close_db

app = FastAPI(
    title="Digital You API",
    description="Autonomous AI agent that acts as your digital representative",
    version="0.1.0"
)

@app.on_event("startup")
async def startup():
    await connect_db()

@app.on_event("shutdown")
async def shutdown():
    await close_db()

@app.get("/ping")
async def ping():
    return {
        "status": "ok",
        "message": "Digital You API is alive!"
    }
from app.core.database import connect_db, close_db, get_db

@app.get("/db-check")
async def db_check():
    db = get_db()
    collections = await db.list_collection_names()
    return {
        "status": "ok",
        "message": "MongoDB is connected!",
        "collections": collections
    }