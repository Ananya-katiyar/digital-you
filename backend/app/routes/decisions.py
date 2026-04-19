from fastapi import APIRouter, HTTPException
from app.core.database import get_db
from datetime import datetime

router = APIRouter()

@router.get("/")
async def get_decisions(email: str, limit: int = 20):
    """
    Returns the last N risk decisions logged for a user.
    This is the audit trail — full visibility into what the system did and why.
    """
    db = get_db()
    cursor = db.decisions.find(
        {"user_email": email},
        {"_id": 0}
    ).sort("timestamp", -1).limit(limit)

    decisions = await cursor.to_list(length=limit)

    # Convert datetime to string for JSON serialisation
    for d in decisions:
        if isinstance(d.get("timestamp"), datetime):
            d["timestamp"] = d["timestamp"].isoformat()

    return {
        "status": "ok",
        "count": len(decisions),
        "decisions": decisions
    }


@router.patch("/{email_id}/reviewed")
async def mark_reviewed(email_id: str, user_email: str):
    """
    Marks a decision as reviewed by the user.
    """
    db = get_db()
    result = await db.decisions.update_one(
        {"email_id": email_id, "user_email": user_email},
        {"$set": {"reviewed": True}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Decision not found")

    return {"status": "ok", "message": "Marked as reviewed"}