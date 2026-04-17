from fastapi import APIRouter
from app.services.calendar import fetch_calendar_events

router = APIRouter()

@router.get("/events")
async def get_calendar_events(email: str):
    events = await fetch_calendar_events(email)
    return {
        "status": "ok",
        "count": len(events),
        "events": events
    }