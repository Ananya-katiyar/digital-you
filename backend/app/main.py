from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import connect_db, close_db, get_db
from app.routes.auth import router as auth_router
from app.routes.emails import router as emails_router
from app.routes.calendar import router as calendar_router
from app.routes.profile import router as profile_router
from app.routes.drafts import router as drafts_router
from app.routes.decisions import router as decisions_router
from app.routes.queue import router as queue_router
from app.routes.tone import router as tone_router
from app.routes.scheduling import router as scheduling_router
from app.routes.learning import router as learning_router
from app.routes.access import router as access_router
from app.routes.send import router as send_router
import os


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

app = FastAPI(
    title="Digital You API",
    description="Autonomous AI agent that acts as your digital representative",
    version="0.1.0"
)

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(emails_router, prefix="/emails", tags=["Emails"])
app.include_router(calendar_router, prefix="/calendar", tags=["Calendar"])
app.include_router(profile_router, prefix="/profile", tags=["Profile"])
app.include_router(drafts_router, prefix="/drafts", tags=["Drafts"])
app.include_router(decisions_router, prefix="/decisions", tags=["Decisions"])
app.include_router(queue_router, prefix="/queue", tags=["Queue"])
app.include_router(tone_router, prefix="/tone", tags=["Tone"])
app.include_router(scheduling_router, prefix="/scheduling", tags=["Scheduling"])
app.include_router(learning_router, prefix="/learning", tags=["Learning"])
app.include_router(access_router, prefix="/access", tags=["Access Control"])
app.include_router(send_router, prefix="/send", tags=["Send"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

@app.get("/db-check")
async def db_check():
    db = get_db()
    collections = await db.list_collection_names()
    return {
        "status": "ok",
        "message": "MongoDB is connected!",
        "collections": collections
    }