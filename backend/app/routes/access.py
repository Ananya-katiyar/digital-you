from fastapi import APIRouter, HTTPException
from app.core.database import get_db
from datetime import datetime, timezone

router = APIRouter()

@router.post("/pause")
async def pause_agent(email: str):
    """
    Pauses the AI agent — no actions taken while paused.
    System still reads emails but won't draft or queue anything.
    """
    db = get_db()
    user = await db.users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.users.update_one(
        {"email": email},
        {"$set": {
            "agent_paused": True,
            "paused_at": datetime.now(timezone.utc)
        }}
    )
    return {"status": "ok", "message": "Agent paused — no automated actions will be taken"}

@router.post("/resume")
async def resume_agent(email: str):
    """Resumes the AI agent after being paused."""
    db = get_db()
    user = await db.users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.users.update_one(
        {"email": email},
        {"$set": {
            "agent_paused": False,
            "paused_at": None
        }}
    )
    return {"status": "ok", "message": "Agent resumed — monitoring your inbox"}

@router.post("/revoke")
async def revoke_access(email: str):
    """
    Revokes all Google OAuth access.
    Deletes stored tokens — user must re-authenticate to use the system.
    """
    db = get_db()
    user = await db.users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.users.update_one(
        {"email": email},
        {"$set": {
            "encrypted_access_token": None,
            "encrypted_refresh_token": None,
            "agent_paused": True,
            "access_revoked": True,
            "revoked_at": datetime.now(timezone.utc)
        }}
    )
    return {
        "status": "ok",
        "message": "Access revoked — all tokens deleted. Re-authenticate to restore access."
    }

@router.get("/status")
async def get_agent_status(email: str):
    """Returns the current agent status for a user."""
    db = get_db()
    user = await db.users.find_one({"email": email}, {"_id": 0})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "status": "ok",
        "agent_paused": user.get("agent_paused", False),
        "access_revoked": user.get("access_revoked", False),
        "paused_at": user.get("paused_at"),
    }