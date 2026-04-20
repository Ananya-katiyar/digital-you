from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.queue import add_to_queue, resolve_queue_item
from app.core.database import get_db
from datetime import datetime

router = APIRouter()

class QueueItemRequest(BaseModel):
    user_email: str
    email_id: str
    subject: str
    snippet: str
    sender: str
    intent: str
    risk_level: str
    risk_reason: str
    draft: str = None

@router.get("/")
async def get_queue(email: str):
    """
    Returns all pending items in the approval queue for a user.
    """
    db = get_db()
    cursor = db.pending_actions.find(
        {"user_email": email, "status": "pending"},
        {"_id": 0}
    ).sort("created_at", -1)

    items = await cursor.to_list(length=50)

    for item in items:
        if isinstance(item.get("created_at"), datetime):
            item["created_at"] = item["created_at"].isoformat()

    return {
        "status": "ok",
        "count": len(items),
        "queue": items
    }


@router.post("/")
async def queue_item(request: QueueItemRequest):
    """
    Manually adds an email to the approval queue.
    """
    result = await add_to_queue(
        user_email=request.user_email,
        email_id=request.email_id,
        subject=request.subject,
        snippet=request.snippet,
        sender=request.sender,
        intent=request.intent,
        risk_level=request.risk_level,
        risk_reason=request.risk_reason,
        draft=request.draft
    )
    return {"status": "ok", **result}


@router.post("/{email_id}/approve")
async def approve_item(email_id: str, user_email: str):
    """
    Approves a queued item — returns the draft for manual sending.
    Never auto-sends. User always clicks send themselves.
    """
    result = await resolve_queue_item(email_id, user_email, "approve")
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return {"status": "ok", **result}


@router.post("/{email_id}/reject")
async def reject_item(email_id: str, user_email: str):
    """
    Rejects a queued item — removes it from the queue, no action taken.
    """
    result = await resolve_queue_item(email_id, user_email, "reject")
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return {"status": "ok", **result}