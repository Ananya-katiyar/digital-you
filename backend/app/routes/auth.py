from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from app.core.encryption import encrypt_token
from app.core.database import get_db
from app.models.user import create_user_document
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/calendar.readonly"
]

def create_flow():
    os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"
    return Flow.from_client_config(
        {
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [GOOGLE_REDIRECT_URI]
            }
        },
        scopes=SCOPES,
        redirect_uri=GOOGLE_REDIRECT_URI
    )

flow_store = {}

@router.get("/google")
async def google_login():
    flow = create_flow()
    auth_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent"
    )
    flow_store[state] = flow
    return RedirectResponse(auth_url)

@router.get("/callback")
async def google_callback(code: str, state: str = None):
    flow = flow_store.get(state)
    if not flow:
        flow = create_flow()
    
    flow.fetch_token(code=code)
    credentials = flow.credentials

    # Get user email from Google
    service = build("oauth2", "v2", credentials=credentials)
    user_info = service.userinfo().get().execute()
    email = user_info.get("email")

    # Encrypt tokens
    encrypted_access_token = encrypt_token(credentials.token)
    encrypted_refresh_token = encrypt_token(credentials.refresh_token) if credentials.refresh_token else None

    # Save to MongoDB
    db = get_db()
    existing_user = await db.users.find_one({"email": email})

    if existing_user:
        await db.users.update_one(
            {"email": email},
            {"$set": {
                "encrypted_access_token": encrypted_access_token,
                "encrypted_refresh_token": encrypted_refresh_token,
            }}
        )
        message = "User updated successfully"
    else:
        user_doc = create_user_document(
            email=email,
            encrypted_access_token=encrypted_access_token,
            encrypted_refresh_token=encrypted_refresh_token,
            scopes=list(credentials.scopes) if credentials.scopes else SCOPES
        )
        await db.users.insert_one(user_doc)
        message = "User created successfully"

    return {
        "status": "success",
        "message": message,
        "email": email,
        "access_token_stored": True,
        "encrypted": True
    }