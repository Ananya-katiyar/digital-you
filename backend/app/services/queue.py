from datetime import datetime, timezone
from app.core.database import get_db

async def add_to_queue(
    user_email: str,
    email_id: str,
    subject: str,
    snippet: str,
    sender: str,
    intent: str,
    risk_level: str,
    risk_reason: str,
    draft: str = None
):
    """
    Adds a medium-risk email to the pending approval queue.
    The system never acts on these without explicit user approval.
    """
    db = get_db()

    # Check if already in queue to avoid duplicates
    existing = await db.pending_actions.find_one({
        "user_email": user_email,
        "email_id": email_id
    })
    if existing:
        return {"already_queued": True}

    item = {
        "user_email": user_email,
        "email_id": email_id,
        "subject": subject,
        "snippet": snippet,
        "sender": sender,
        "intent": intent,
        "risk_level": risk_level,
        "risk_reason": risk_reason,
        "draft": draft,
        "status": "pending",       # pending | approved | rejected
        "created_at": datetime.now(timezone.utc),
        "resolved_at": None,
        "resolved_by": "user"
    }

    await db.pending_actions.insert_one(item)
    return {"queued": True}


async def resolve_queue_item(
    email_id: str,
    user_email: str,
    action: str         # "approve" or "reject"
) -> dict:
    """
    Resolves a pending queue item as approved or rejected.
    Returns the item so the caller can use the draft if approved.
    """
    db = get_db()

    item = await db.pending_actions.find_one({
        "email_id": email_id,
        "user_email": user_email,
        "status": "pending"
    })

    if not item:
        return {"error": "Item not found or already resolved"}

    await db.pending_actions.update_one(
        {"email_id": email_id, "user_email": user_email},
        {"$set": {
            "status": action + "d",   # "approved" or "rejected"
            "resolved_at": datetime.now(timezone.utc)
        }}
    )

    return {
        "resolved": True,
        "action": action,
        "subject": item.get("subject"),
        "draft": item.get("draft") if action == "approve" else None,
        "message": "Draft is ready to send manually." if action == "approve" else "Email rejected and removed from queue."
    }