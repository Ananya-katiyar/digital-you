from fastapi import APIRouter, HTTPException
from app.core.database import get_db
from app.models.profile import UpdateProfileRequest
from datetime import datetime, timezone

router = APIRouter()

@router.get("/")
async def get_profile(email: str):
    db = get_db()
    user = await db.users.find_one({"email": email})
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "status": "ok",
        "email": user["email"],
        "preferences": user.get("preferences", {}),
        "scopes_granted": user.get("scopes_granted", []),
        "created_at": user.get("created_at"),
        "updated_at": user.get("updated_at")
    }

@router.patch("/")
async def update_profile(email: str, updates: UpdateProfileRequest):
    db = get_db()
    user = await db.users.find_one({"email": email})
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    current_preferences = user.get("preferences", {})
    update_data = updates.model_dump(exclude_none=True)
    
    for key, value in update_data.items():
        current_preferences[key] = value
    
    await db.users.update_one(
        {"email": email},
        {"$set": {
            "preferences": current_preferences,
            "updated_at": datetime.now(timezone.utc)
        }}
    )
    
    return {
        "status": "ok",
        "message": "Profile updated successfully",
        "email": email,
        "updated_preferences": current_preferences
    }