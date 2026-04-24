from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.llm import generate_draft_reply
from app.services.nlp import detect_intent
from app.services.scheduling import suggest_meeting_slots
from app.core.database import get_db

router = APIRouter()

class DraftRequest(BaseModel):
    subject: str
    snippet: str
    tone: str = "professional"
    user_email: str = None

@router.post("/")
async def create_draft(request: DraftRequest):
    """
    Generates a draft reply using the LLM.
    If intent is scheduling, also suggests free time slots.
    Uses tone profile if available for personalised replies.
    """
    intent = detect_intent(request.subject, request.snippet)

    # Load tone profile from MongoDB if user_email provided
    tone_profile = None
    if request.user_email:
        db = get_db()
        user = await db.users.find_one({"email": request.user_email})
        if user:
            tone_profile = user.get("tone_profile")

    # Generate the draft reply
    draft = await generate_draft_reply(
        subject=request.subject,
        snippet=request.snippet,
        tone=request.tone,
        intent=intent,
        tone_profile=tone_profile
    )

    response = {
        "status": "ok",
        "intent": intent,
        "tone": request.tone,
        "tone_profile_used": tone_profile is not None,
        "draft": draft
    }

    # For scheduling emails — also suggest free slots
    if intent == "scheduling" and request.user_email:
        scheduling = await suggest_meeting_slots(
            user_email=request.user_email,
            tone=request.tone
        )
        response["scheduling_suggestions"] = scheduling

    return response