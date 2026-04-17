from datetime import datetime, timezone

def create_user_document(email: str, encrypted_access_token: str, encrypted_refresh_token: str, scopes: list):
    return {
        "email": email,
        "encrypted_access_token": encrypted_access_token,
        "encrypted_refresh_token": encrypted_refresh_token,
        "scopes_granted": scopes,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
        "preferences": {
            "tone": "professional",
            "afk_mode": False,
            "timezone": "Asia/Kolkata",
            "rules": []
        }
    }