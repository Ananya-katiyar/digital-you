from fastapi import APIRouter
from app.services.gmail import fetch_emails

router = APIRouter()

@router.get("/")
async def get_emails(email: str):
    emails = await fetch_emails(email)
    return {
        "status": "ok",
        "count": len(emails),
        "emails": emails
    }