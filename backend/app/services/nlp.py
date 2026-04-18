import spacy
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

nlp = spacy.load("en_core_web_sm")
summarizer = LexRankSummarizer()

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
    "click here", "free shipping", "free trial", "coupon", "promo",
    "newsletter", "no-reply", "noreply", "marketing", "subscription",
    "% off"
],
}

def detect_intent(subject: str, snippet: str, sender: str = "") -> str:
    """
    Classifies an email into one of four intents:
    casual | scheduling | urgent | promotional
    """
    text = f"{subject} {snippet} {sender}".lower()

    for keyword in INTENT_PATTERNS["promotional"]:
        if keyword in text:
            return "promotional"

    for keyword in INTENT_PATTERNS["urgent"]:
        if keyword in text:
            return "urgent"

    for keyword in INTENT_PATTERNS["scheduling"]:
        if keyword in text:
            return "scheduling"

    return "casual"


def extract_entities(subject: str, snippet: str) -> list:
    """
    Extracts named entities (people, dates, orgs, locations)
    using spaCy NER.
    """
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
    return entities


def summarise_text(text: str, sentence_count: int = 1) -> str:
    """
    Generates a short summary using LexRank algorithm (offline).
    Falls back to first 100 chars if text is too short to summarise.
    """
    # sumy needs at least 2 sentences to work properly
    if len(text.split(".")) < 2:
        return text[:150].strip()

    try:
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summary_sentences = summarizer(parser.document, sentence_count)
        return " ".join(str(s) for s in summary_sentences).strip()
    except Exception:
        return text[:150].strip()


def analyse_email(subject: str, snippet: str, sender: str = "") -> dict:
    """
    Runs full NLP analysis on an email.
    Returns intent, named entities, and a short summary.
    """
    intent = detect_intent(subject, snippet, sender)
    entities = extract_entities(subject, snippet)
    summary = summarise_text(f"{subject}. {snippet}")

    return {
        "intent": intent,
        "entities": entities,
        "summary": summary
    }