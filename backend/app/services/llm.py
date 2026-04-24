from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate

# Initialise the local Ollama model
llm = OllamaLLM(model="mistral", temperature=0.7)

# Enhanced prompt that uses tone profile signals
REPLY_PROMPT = PromptTemplate(
    input_variables=[
        "subject", "snippet", "tone", "intent",
        "formality", "avg_sentence_length", "greeting_style",
        "signoff_style", "uses_exclamations"
    ],
    template="""
You are acting as a digital assistant drafting a reply on behalf of the user.

Email details:
- Subject: {subject}
- Message: {snippet}
- Detected intent: {intent}

User's writing style (learned from their past emails):
- Formality level: {formality}
- Average sentence length: {avg_sentence_length} words
- Greeting style: {greeting_style}
- Sign-off style: {signoff_style}
- Uses exclamations: {uses_exclamations}

Instructions:
- Write a reply in a {tone} tone that matches the user's natural writing style
- Mirror their formality level and sentence length
- Keep it concise (2-4 sentences maximum)
- Do NOT make any commitments, promises, or confirm any meetings
- Do NOT include a subject line
- Do NOT include placeholders like [Name] or [Your Name]
- Just write the reply body, nothing else

Draft reply:
"""
)


async def generate_draft_reply(
    subject: str,
    snippet: str,
    tone: str = "professional",
    intent: str = "casual",
    tone_profile: dict = None
) -> str:
    """
    Generates a draft email reply using the local Mistral model.
    Now uses tone profile signals for personalised replies.
    """
    # Use tone profile if available, otherwise use safe defaults
    if tone_profile:
        formality = tone_profile.get("formality", "professional")
        avg_sentence_length = tone_profile.get("avg_sentence_length", 12)
        greeting_style = tone_profile.get("greeting_style", "neutral")
        signoff_style = tone_profile.get("signoff_style", "neutral")
        uses_exclamations = str(tone_profile.get("uses_exclamations", False))
    else:
        formality = tone
        avg_sentence_length = 12
        greeting_style = "neutral"
        signoff_style = "neutral"
        uses_exclamations = "False"

    try:
        chain = REPLY_PROMPT | llm
        response = await chain.ainvoke({
            "subject": subject,
            "snippet": snippet,
            "tone": tone,
            "intent": intent,
            "formality": formality,
            "avg_sentence_length": avg_sentence_length,
            "greeting_style": greeting_style,
            "signoff_style": signoff_style,
            "uses_exclamations": uses_exclamations
        })
        return response.strip()
    except Exception as e:
        return f"Draft generation failed: {str(e)}"