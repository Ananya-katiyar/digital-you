from fastapi import APIRouter
from app.services.gmail import fetch_emails
from app.services.nlp import analyse_email

router = APIRouter()

@router.get("/")
async def get_emails(email: str):
    emails = await fetch_emails(email)

    for mail in emails:
        mail["analysis"] = analyse_email(
            subject=mail.get("subject", ""),
            snippet=mail.get("snippet", ""),
            sender=mail.get("sender", "")
        )

    return {
        "status": "ok",
        "count": len(emails),
        "emails": emails
    }