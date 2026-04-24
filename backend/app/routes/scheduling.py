from fastapi import APIRouter
from app.services.scheduling import suggest_meeting_slots

router = APIRouter()

@router.get("/suggest")
async def suggest_slots(email: str, tone: str = "professional"):
    """
    Suggests 3 free meeting slots based on calendar availability.
    Never auto-confirms anything — suggestions only.
    """
    result = await suggest_meeting_slots(email, tone)
    return {
        "status": "ok",
        **result
    }