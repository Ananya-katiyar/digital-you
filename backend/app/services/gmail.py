from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from app.core.encryption import decrypt_token, encrypt_token
from app.core.database import get_db
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

async def get_credentials(email: str):
    db = get_db()
    user = await db.users.find_one({"email": email})
    if not user:
        return None

    access_token = decrypt_token(user["encrypted_access_token"])
    refresh_token = decrypt_token(user["encrypted_refresh_token"]) if user.get("encrypted_refresh_token") else None

    credentials = Credentials(
        token=access_token,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET
    )

    if credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
        await db.users.update_one(
            {"email": email},
            {"$set": {
                "encrypted_access_token": encrypt_token(credentials.token)
            }}
        )

    return credentials

async def fetch_emails(email: str):
    credentials = await get_credentials(email)
    if not credentials:
        return {"error": "User not found"}

    service = build("gmail", "v1", credentials=credentials)
    results = service.users().messages().list(
        userId="me",
        maxResults=10,
        labelIds=["INBOX"]
    ).execute()

    messages = results.get("messages", [])
    emails = []

    for msg in messages:
        msg_detail = service.users().messages().get(
            userId="me",
            id=msg["id"],
            format="metadata",
            metadataHeaders=["From", "Subject", "Date"]
        ).execute()

        headers = msg_detail.get("payload", {}).get("headers", [])
        header_map = {h["name"]: h["value"] for h in headers}

        emails.append({
            "id": msg["id"],
            "subject": header_map.get("Subject", "No Subject"),
            "sender": header_map.get("From", "Unknown"),
            "date": header_map.get("Date", ""),
            "snippet": msg_detail.get("snippet", "")
        })

    return emails