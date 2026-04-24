from fastapi import APIRouter, HTTPException
from app.services.tone_analyser import build_tone_profile
from app.core.database import get_db

router = APIRouter()

@router.post("/analyse")
async def analyse_tone(email: str):
    """
    Analyses the user's writing style from their sent emails.
    Stores tone profile in MongoDB for use in draft generation.
    """
    profile = await build_tone_profile(email)
    return {
        "status": "ok",
        "message": "Tone profile built successfully",
        "tone_profile": profile
    }

@router.get("/profile")
async def get_tone_profile(email: str):
    """
    Returns the stored tone profile for a user.
    """
    db = get_db()
    user = await db.users.find_one({"email": email}, {"_id": 0, "tone_profile": 1})

    if not user or "tone_profile" not in user:
        raise HTTPException(
            status_code=404,
            detail="No tone profile found. Call POST /tone/analyse first."
        )

    return {
        "status": "ok",
        "tone_profile": user["tone_profile"]
    }