from datetime import datetime, timezone
from app.core.database import get_db


async def log_correction(
    user_email: str,
    email_id: str,
    subject: str,
    original_draft: str,
    corrected_draft: str,
    intent: str,
    tone: str
):
    """
    Logs a user correction when they edit an AI draft.
    This builds a corrections dataset for improving future drafts.
    """
    db = get_db()

    correction = {
        "user_email": user_email,
        "email_id": email_id,
        "subject": subject,
        "original_draft": original_draft,
        "corrected_draft": corrected_draft,
        "intent": intent,
        "tone": tone,
        "timestamp": datetime.now(timezone.utc),
        "applied": False  # will be True once used in a prompt
    }

    await db.corrections.insert_one(correction)
    return {"logged": True}


async def get_recent_corrections(user_email: str, limit: int = 3) -> list:
    """
    Fetches the user's most recent corrections to inject
    into the LLM prompt as few-shot examples.
    """
    db = get_db()
    cursor = db.corrections.find(
        {"user_email": user_email},
        {"_id": 0}
    ).sort("timestamp", -1).limit(limit)

    corrections = await cursor.to_list(length=limit)
    return corrections