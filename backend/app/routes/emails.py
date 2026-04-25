from fastapi import APIRouter
from app.services.gmail import fetch_emails
from app.services.nlp import analyse_email
from app.services.risk import classify_risk
from app.services.decisions import log_decision
from app.services.queue import add_to_queue
from app.core.database import get_db

router = APIRouter()

@router.get("/")
async def get_emails(email: str):
    db = get_db()
    user = await db.users.find_one({"email": email})
    user_rules = []

    if user:
    # Check if agent is paused

        if user.get("agent_paused", False):
            return {
                "status": "paused",
                "message": "Agent is paused — resume from your profile to enable monitoring",
                "count": 0,
                "emails": []
            }

        prefs = user.get("preferences", {})
        afk_mode = prefs.get("afk_mode", False)
        raw_rules = prefs.get("rules", [])
        user_rules = raw_rules if raw_rules else []
    else:
        afk_mode = False

    emails = await fetch_emails(email)

    for mail in emails:
        subject = mail.get("subject", "")
        snippet = mail.get("snippet", "")
        sender = mail.get("sender", "")
        email_id = mail.get("id", "")

        # NLP analysis
        analysis = analyse_email(subject, snippet, sender)

        # Risk classification
        risk = classify_risk(
            subject=subject,
            snippet=snippet,
            intent=analysis["intent"],
            entities=analysis["entities"],
            user_rules=user_rules
        )

        # Log the decision to MongoDB
        await log_decision(
            user_email=email,
            email_id=email_id,
            subject=subject,
            intent=analysis["intent"],
            risk_level=risk["risk_level"],
            risk_reason=risk["risk_reason"],
            action=risk["action"]
        )

        # Queue medium-risk items (or all non-low if AFK mode is on)
        should_queue = (
            risk["risk_level"] == "medium" or
            (afk_mode and risk["risk_level"] != "low")
        )

        if should_queue:
            await add_to_queue(
                user_email=email,
                email_id=email_id,
                subject=subject,
                snippet=snippet,
                sender=sender,
                intent=analysis["intent"],
                risk_level=risk["risk_level"],
                risk_reason=risk["risk_reason"],
                draft=None  # Draft generated separately via POST /drafts/
            )

        mail["analysis"] = analysis
        mail["risk"] = risk

    return {
        "status": "ok",
        "count": len(emails),
        "emails": emails
    }