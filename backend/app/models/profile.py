from pydantic import BaseModel
from typing import Optional, List

class UserRule(BaseModel):
    id: Optional[str] = None
    description: str          # Human readable e.g. "Don't schedule after 6 PM"
    rule_type: str            # "time_based" | "topic_based" | "sender_based"
    condition: str            # "after_6pm" | "hr_topics" | "legal" | "financial"
    action: str = "escalate"  # What to do when triggered

class UserPreferences(BaseModel):
    tone: Optional[str] = "professional"
    afk_mode: Optional[bool] = False
    timezone: Optional[str] = "Asia/Kolkata"
    rules: Optional[List[UserRule]] = []

class ProfileResponse(BaseModel):
    email: str
    preferences: UserPreferences
    scopes_granted: Optional[List[str]] = []

class UpdateProfileRequest(BaseModel):
    tone: Optional[str] = None
    afk_mode: Optional[bool] = None
    timezone: Optional[str] = None
    rules: Optional[List[UserRule]] = None