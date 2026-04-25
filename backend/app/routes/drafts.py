from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.llm import generate_draft_reply
from app.services.nlp import detect_intent
from app.services.scheduling import suggest_meeting_slots
from app.services.learning import get_recent_corrections
from app.core.database import get_db

router = APIRouter()

class DraftRequest(BaseModel):
    subject: str
    snippet: str
    tone: str = "professional"
    user_email: str = None

@router.post("/")
async def create_draft(request: DraftRequest):
    intent = detect_intent(request.subject, request.snippet)

    tone_profile = None
    corrections = []

    if request.user_email:
        db = get_db()
        user = await db.users.find_one({"email": request.user_email})
        if user:
            tone_profile = user.get("tone_profile")

        # Load recent corrections for few-shot learning
        corrections = await get_recent_corrections(request.user_email, limit=3)

    draft = await generate_draft_reply(
        subject=request.subject,
        snippet=request.snippet,
        tone=request.tone,
        intent=intent,
        tone_profile=tone_profile,
        corrections=corrections
    )

    response = {
        "status": "ok",
        "intent": intent,
        "tone": request.tone,
        "tone_profile_used": tone_profile is not None,
        "corrections_used": len(corrections),
        "draft": draft
    }

    if intent == "scheduling" and request.user_email:
        scheduling = await suggest_meeting_slots(
            user_email=request.user_email,
            tone=request.tone
        )
        response["scheduling_suggestions"] = scheduling

    return response