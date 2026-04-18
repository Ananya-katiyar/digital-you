import spacy
import re

nlp = spacy.load("en_core_web_sm")

# Intent keyword patterns
INTENT_PATTERNS = {
    "scheduling": [
        "meet", "meeting", "schedule", "call", "catch up", "available",
        "availability", "time slot", "calendar", "tomorrow", "next week",
        "sync", "discuss", "appointment", "book", "reschedule"
    ],
    "urgent": [
        "urgent", "asap", "immediately", "deadline", "critical", "important",
        "action required", "respond", "emergency", "by eod", "by end of day",
        "time sensitive", "priority", "overdue"
    ],
    "promotional": [
        "unsubscribe", "offer", "deal", "discount", "sale", "limited time",
        "click here", "free", "% off", "coupon", "promo", "newsletter",
        "no-reply", "noreply", "marketing", "subscription"
    ]
}

def detect_intent(subject: str, snippet: str, sender: str = "") -> str:
    """
    Classifies an email into one of four intents:
    casual | scheduling | urgent | promotional
    """
    text = f"{subject} {snippet} {sender}".lower()

    # Check promotional first (sender patterns are strong signals)
    for keyword in INTENT_PATTERNS["promotional"]:
        if keyword in text:
            return "promotional"

    # Check urgent
    for keyword in INTENT_PATTERNS["urgent"]:
        if keyword in text:
            return "urgent"

    # Check scheduling
    for keyword in INTENT_PATTERNS["scheduling"]:
        if keyword in text:
            return "scheduling"

    # Default to casual
    return "casual"


def analyse_email(subject: str, snippet: str, sender: str = "") -> dict:
    """
    Runs full NLP analysis on an email.
    Returns intent, named entities, and a short summary.
    """
    intent = detect_intent(subject, snippet, sender)

    # Named entity recognition using spaCy
    doc = nlp(f"{subject}. {snippet}")
    entities = []
    seen = set()
    for ent in doc.ents:
        if ent.label_ in ("PERSON", "ORG", "DATE", "TIME", "GPE") and ent.text not in seen:
            entities.append({
                "text": ent.text,
                "label": ent.label_
            })
            seen.add(ent.text)

    return {
        "intent": intent,
        "entities": entities,
    }