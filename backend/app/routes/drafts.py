from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.llm import generate_draft_reply
from app.services.nlp import detect_intent

router = APIRouter()

class DraftRequest(BaseModel):
    subject: str
    snippet: str
    tone: str = "professional"

@router.post("/")
async def create_draft(request: DraftRequest):
    intent = detect_intent(request.subject, request.snippet)

    draft = await generate_draft_reply(
        subject=request.subject,
        snippet=request.snippet,
        tone=request.tone,
        intent=intent
    )

    return {
        "status": "ok",
        "intent": intent,
        "tone": request.tone,
        "draft": draft
    }