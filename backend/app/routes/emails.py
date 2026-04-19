from fastapi import APIRouter
from app.services.gmail import fetch_emails
from app.services.nlp import analyse_email
from app.services.risk import classify_risk

router = APIRouter()

@router.get("/")
async def get_emails(email: str):
    emails = await fetch_emails(email)

    for mail in emails:
        analysis = analyse_email(
            subject=mail.get("subject", ""),
            snippet=mail.get("snippet", ""),
            sender=mail.get("sender", "")
        )

        risk = classify_risk(
            subject=mail.get("subject", ""),
            snippet=mail.get("snippet", ""),
            intent=analysis["intent"],
            entities=analysis["entities"],
            user_rules=[]
        )

        mail["analysis"] = analysis
        mail["risk"] = risk

    return {
        "status": "ok",
        "count": len(emails),
        "emails": emails
    }