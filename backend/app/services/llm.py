from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate


# Initialise the local Ollama model
# Using mistral — good quality, runs on CPU with 16GB RAM
llm = OllamaLLM(model="mistral", temperature=0.7)

# Prompt template for reply drafting
REPLY_PROMPT = PromptTemplate(
    input_variables=["subject", "snippet", "tone", "intent"],
    template="""
You are acting as a digital assistant drafting a reply on behalf of the user.

Email details:
- Subject: {subject}
- Message: {snippet}
- Detected intent: {intent}

Instructions:
- Write a reply in a {tone} tone
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
    intent: str = "casual"
) -> str:
    """
    Generates a draft email reply using the local Mistral model.
    Returns the draft as a plain string.
    """
    try:
        chain = REPLY_PROMPT | llm
        response = await chain.ainvoke({
            "subject": subject,
            "snippet": snippet,
            "tone": tone,
            "intent": intent
        })
        return response.strip()
    except Exception as e:
        return f"Draft generation failed: {str(e)}"