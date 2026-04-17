from googleapiclient.discovery import build
from app.services.gmail import get_credentials
from datetime import datetime, timezone, timedelta

async def fetch_calendar_events(email: str):
    credentials = await get_credentials(email)
    if not credentials:
        return {"error": "User not found"}

    service = build("calendar", "v3", credentials=credentials)
    
    now = datetime.now(timezone.utc)
    seven_days_later = now + timedelta(days=7)

    events_result = service.events().list(
        calendarId="primary",
        timeMin=now.isoformat(),
        timeMax=seven_days_later.isoformat(),
        maxResults=20,
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    events = events_result.get("items", [])
    calendar_events = []

    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        end = event["end"].get("dateTime", event["end"].get("date"))

        calendar_events.append({
            "id": event["id"],
            "title": event.get("summary", "No Title"),
            "start": start,
            "end": end,
            "location": event.get("location", ""),
            "description": event.get("description", ""),
            "attendees": [
                a.get("email") for a in event.get("attendees", [])
            ]
        })

    return calendar_events
