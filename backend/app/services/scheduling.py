from datetime import datetime, timezone, timedelta
from app.services.calendar import fetch_calendar_events


def get_free_slots(events: list, days_ahead: int = 5) -> list:
    """
    Analyses calendar events and suggests 3 free time slots.
    Works within business hours (9 AM - 6 PM) only.
    Never auto-confirms anything — suggestions only.
    """
    now = datetime.now(timezone.utc)
    suggestions = []

    # Business hours: 9 AM to 6 PM
    WORK_START = 9
    WORK_END = 18
    SLOT_DURATION = 60  # minutes

    # Build list of busy periods from existing events
    busy_periods = []
    for event in events:
        start_str = event.get("start", "")
        end_str = event.get("end", "")

        if not start_str or not end_str:
            continue

        try:
            # Handle both date and datetime formats
            if "T" in start_str:
                start = datetime.fromisoformat(start_str.replace("Z", "+00:00"))
                end = datetime.fromisoformat(end_str.replace("Z", "+00:00"))
            else:
                # All-day event — mark entire day as busy
                start = datetime.fromisoformat(start_str).replace(
                    hour=WORK_START, minute=0, tzinfo=timezone.utc
                )
                end = datetime.fromisoformat(start_str).replace(
                    hour=WORK_END, minute=0, tzinfo=timezone.utc
                )
            busy_periods.append((start, end))
        except Exception:
            continue

    # Scan next N days for free slots
    for day_offset in range(1, days_ahead + 1):
        target_date = now + timedelta(days=day_offset)

        # Skip weekends
        if target_date.weekday() >= 5:
            continue

        # Scan business hours in 1-hour increments
        for hour in range(WORK_START, WORK_END - 1):
            slot_start = target_date.replace(
                hour=hour, minute=0, second=0, microsecond=0
            )
            slot_end = slot_start + timedelta(minutes=SLOT_DURATION)

            # Check if slot overlaps with any busy period
            is_free = True
            for busy_start, busy_end in busy_periods:
                if slot_start < busy_end and slot_end > busy_start:
                    is_free = False
                    break

            if is_free:
                suggestions.append({
                    "date": slot_start.strftime("%A, %B %d"),
                    "start_time": slot_start.strftime("%I:%M %p"),
                    "end_time": slot_end.strftime("%I:%M %p"),
                    "iso_start": slot_start.isoformat(),
                    "iso_end": slot_end.isoformat()
                })

            # Stop once we have 3 suggestions
            if len(suggestions) >= 3:
                return suggestions

    return suggestions


def format_scheduling_response(slots: list, tone: str = "professional") -> str:
    """
    Formats suggested time slots into a natural language response.
    Always frames these as suggestions — never confirmations.
    """
    if not slots:
        return (
            "I currently don't have any free slots available in the next few days. "
            "Could you suggest a time that works for you and I'll check my availability?"
        )

    if tone == "casual":
        intro = "Hey! Here are a few times that could work for me:"
        outro = "Let me know which one works for you and we can sort it out!"
    else:
        intro = "Thank you for reaching out. Here are a few available time slots:"
        outro = (
            "Please let me know which time works best for you and "
            "I will confirm the details shortly."
        )

    slot_lines = []
    for i, slot in enumerate(slots, 1):
        slot_lines.append(
            f"{i}. {slot['date']} — {slot['start_time']} to {slot['end_time']}"
        )

    return f"{intro}\n\n" + "\n".join(slot_lines) + f"\n\n{outro}"


async def suggest_meeting_slots(user_email: str, tone: str = "professional") -> dict:
    """
    Main function — fetches calendar, finds free slots,
    formats a natural language scheduling suggestion.
    Never auto-confirms. Always returns suggestions only.
    """
    events = await fetch_calendar_events(user_email)

    if isinstance(events, dict) and "error" in events:
        return {
            "error": "Could not fetch calendar",
            "slots": [],
            "suggestion": None
        }

    free_slots = get_free_slots(events)
    suggestion = format_scheduling_response(free_slots, tone)

    return {
        "slots_found": len(free_slots),
        "suggested_slots": free_slots,
        "draft_response": suggestion,
        "note": "These are suggestions only. Nothing has been confirmed or booked."
    }