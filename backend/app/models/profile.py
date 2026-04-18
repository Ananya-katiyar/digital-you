from pydantic import BaseModel
from typing import Optional, List

class UserPreferences(BaseModel):
    tone: Optional[str] = "professional"
    afk_mode: Optional[bool] = False
    timezone: Optional[str] = "Asia/Kolkata"
    rules: Optional[List[str]] = []

class ProfileResponse(BaseModel):
    email: str
    preferences: UserPreferences
    scopes_granted: Optional[List[str]] = []

class UpdateProfileRequest(BaseModel):
    tone: Optional[str] = None
    afk_mode: Optional[bool] = None
    timezone: Optional[str] = None
    rules: Optional[List[str]] = None