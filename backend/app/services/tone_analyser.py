import re
from datetime import datetime, timezone
from app.services.gmail import fetch_sent_emails
from app.core.database import get_db


def analyse_tone_from_texts(texts: list) -> dict:
    """
    Analyses writing style patterns from a list of email texts.
    Extracts: formality level, avg sentence length, greeting style,
    sign-off style, common phrases.
    All processed locally — no data sent anywhere.
    """
    if not texts:
        return _default_tone_profile()

    all_sentences = []
    all_words = []
    greetings = []
    signoffs = []
    exclamation_count = 0
    question_count = 0
    total_chars = 0

    # Formal and casual word lists
    formal_words = [
        "please", "kindly", "regarding", "hereby", "attached",
        "sincerely", "best regards", "thank you", "appreciate",
        "would you", "could you", "i wanted to"
    ]
    casual_words = [
        "hey", "hi", "yeah", "yep", "nope", "thanks", "cool",
        "awesome", "sure", "ok", "okay", "catch up", "cheers"
    ]

    formal_hits = 0
    casual_hits = 0

    for text in texts:
        text_lower = text.lower()
        total_chars += len(text)

        # Count sentences
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 5]
        all_sentences.extend(sentences)

        # Count words
        words = text.split()
        all_words.extend(words)

        # Exclamation and question marks
        exclamation_count += text.count("!")
        question_count += text.count("?")

        # Detect greeting style (first line)
        first_line = text.split("\n")[0].lower().strip()
        if any(g in first_line for g in ["hey", "hi ", "hello"]):
            greetings.append("casual")
        elif any(g in first_line for g in ["dear", "good morning", "good afternoon"]):
            greetings.append("formal")

        # Detect sign-off style (last non-empty line)
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        if lines:
            last_line = lines[-1].lower()
            if any(s in last_line for s in ["sincerely", "regards", "best regards"]):
                signoffs.append("formal")
            elif any(s in last_line for s in ["thanks", "cheers", "take care", "talk soon"]):
                signoffs.append("casual")

        # Formality scoring
        for word in formal_words:
            if word in text_lower:
                formal_hits += 1
        for word in casual_words:
            if word in text_lower:
                casual_hits += 1

    # Calculate metrics
    avg_sentence_length = (
        sum(len(s.split()) for s in all_sentences) / len(all_sentences)
        if all_sentences else 10
    )

    avg_email_length = total_chars / len(texts) if texts else 0

    # Determine formality
    if formal_hits > casual_hits * 1.5:
        formality = "formal"
    elif casual_hits > formal_hits * 1.5:
        formality = "casual"
    else:
        formality = "professional"

    # Dominant greeting and signoff
    dominant_greeting = (
        max(set(greetings), key=greetings.count) if greetings else "neutral"
    )
    dominant_signoff = (
        max(set(signoffs), key=signoffs.count) if signoffs else "neutral"
    )

    # Emoji/exclamation tendency
    uses_exclamations = exclamation_count > len(texts) * 0.5

    return {
        "formality": formality,
        "avg_sentence_length": round(avg_sentence_length, 1),
        "avg_email_length": round(avg_email_length, 1),
        "greeting_style": dominant_greeting,
        "signoff_style": dominant_signoff,
        "uses_exclamations": uses_exclamations,
        "emails_analysed": len(texts),
        "analysed_at": datetime.now(timezone.utc).isoformat()
    }


def _default_tone_profile() -> dict:
    """Returns a safe default when no sent emails are available"""
    return {
        "formality": "professional",
        "avg_sentence_length": 12.0,
        "avg_email_length": 200.0,
        "greeting_style": "neutral",
        "signoff_style": "neutral",
        "uses_exclamations": False,
        "emails_analysed": 0,
        "analysed_at": datetime.now(timezone.utc).isoformat()
    }


async def build_tone_profile(user_email: str) -> dict:
    """
    Fetches sent emails, analyses tone, and stores
    the profile in MongoDB for future use.
    """
    db = get_db()

    # Fetch sent emails
    sent_texts = await fetch_sent_emails(user_email, max_results=20)

    if isinstance(sent_texts, dict) and "error" in sent_texts:
        return _default_tone_profile()

    # Analyse tone
    profile = analyse_tone_from_texts(sent_texts)

    # Store in MongoDB
    await db.users.update_one(
        {"email": user_email},
        {"$set": {"tone_profile": profile}},
        upsert=False
    )

    return profile