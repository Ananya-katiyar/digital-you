from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.learning import log_correction, get_recent_corrections

router = APIRouter()

class CorrectionRequest(BaseModel):
    user_email: str
    email_id: str
    subject: str
    original_draft: str
    corrected_draft: str
    intent: str
    tone: str = "professional"

@router.post("/correct")
async def submit_correction(request: CorrectionRequest):
    """
    User submits a corrected version of an AI draft.
    Stored as a learning example for future prompts.
    """
    if not request.corrected_draft.strip():
        raise HTTPException(status_code=400, detail="Corrected draft cannot be empty")

    result = await log_correction(
        user_email=request.user_email,
        email_id=request.email_id,
        subject=request.subject,
        original_draft=request.original_draft,
        corrected_draft=request.corrected_draft,
        intent=request.intent,
        tone=request.tone
    )
    return {"status": "ok", **result}

@router.get("/corrections")
async def get_corrections(email: str, limit: int = 10):
    """
    Returns the user's correction history.
    """
    corrections = await get_recent_corrections(email, limit)
    for c in corrections:
        if hasattr(c.get("timestamp"), "isoformat"):
            c["timestamp"] = c["timestamp"].isoformat()
    return {
        "status": "ok",
        "count": len(corrections),
        "corrections": corrections
    }