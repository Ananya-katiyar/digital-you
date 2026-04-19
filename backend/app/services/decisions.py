from datetime import datetime, timezone
from app.core.database import get_db

async def log_decision(
    user_email: str,
    email_id: str,
    subject: str,
    intent: str,
    risk_level: str,
    risk_reason: str,
    action: str
):
    """
    Logs every risk classification decision to MongoDB.
    Creates a full audit trail the user can review.
    """
    db = get_db()
    decision = {
        "user_email": user_email,
        "email_id": email_id,
        "subject": subject,
        "intent": intent,
        "risk_level": risk_level,
        "risk_reason": risk_reason,
        "action": action,
        "timestamp": datetime.now(timezone.utc),
        "reviewed": False
    }
    await db.decisions.insert_one(decision)