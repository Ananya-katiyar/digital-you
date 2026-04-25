from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.gmail import send_email

router = APIRouter()

class SendRequest(BaseModel):
    user_email: str
    to: str
    subject: str
    body: str

@router.post("/")
async def send_reply(request: SendRequest):
    """
    Sends an email reply via Gmail API.
    Only triggered by explicit user action — never automated.
    """
    if not request.body.strip():
        raise HTTPException(status_code=400, detail="Email body cannot be empty")

    if not request.to.strip():
        raise HTTPException(status_code=400, detail="Recipient email is required")

    result = await send_email(
        user_email=request.user_email,
        to=request.to,
        subject=request.subject,
        body=request.body
    )

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return {"status": "ok", **result}