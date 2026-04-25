from datetime import datetime, timezone

# High risk keywords — these topics should never be acted on automatically
HIGH_RISK_KEYWORDS = [
    # Financial
    "salary", "payment", "invoice", "bank", "transfer", "refund",
    "compensation", "budget", "financial", "money", "wire",
    # Legal
    "legal", "contract", "lawsuit", "attorney", "lawyer", "settlement",
    "liability", "compliance", "gdpr", "terms",
    # HR / personal
    "resignation", "terminate", "fired", "complaint", "harassment",
    "disciplinary", "performance review", "hr", "human resources",
    # Medical / sensitive
    "medical", "diagnosis", "prescription", "insurance", "emergency",
    # Security
    "password", "credentials", "otp", "verification code", "2fa",
    "account access", "suspicious", "breach"
]

# Medium risk keywords — need user approval before acting
MEDIUM_RISK_KEYWORDS = [
    "confirm", "agree", "accept", "approve", "decision",
    "deadline", "commitment", "promise", "guarantee", "sign",
    "interview", "offer", "proposal", "negotiat"
]

def check_user_rules(text: str, rules: list, current_hour: int = None) -> dict:
    """
    Applies structured user-defined rules on top of base risk classification.
    Each rule has: description, rule_type, condition, action
    """
    if current_hour is None:
        current_hour = datetime.now(timezone.utc).hour

    for rule in rules:
        # Skip plain strings — old format, not structured rules
        if isinstance(rule, str):
            continue

        # Support both dict (from MongoDB) and Pydantic model
        if hasattr(rule, "condition"):
            condition = rule.condition.lower()
            description = rule.description
        else:
            condition = rule.get("condition", "").lower()
            description = rule.get("description", "")
    return {"triggered": False, "reason": None, "override_level": None}

def classify_risk(
    subject: str,
    snippet: str,
    intent: str,
    entities: list,
    user_rules: list = []
) -> dict:
    """
    Classifies an email into low / medium / high risk.

    Low    → safe to auto-draft a reply
    Medium → suggest reply, wait for user approval
    High   → no action, escalate to user immediately
    """
    text = f"{subject} {snippet}".lower()

    # --- Check high risk keywords first ---
    for keyword in HIGH_RISK_KEYWORDS:
        if keyword in text:
            return {
                "risk_level": "high",
                "risk_reason": f"High-risk keyword detected: '{keyword}'",
                "action": "escalate"
            }

    # --- Check user-defined rules ---
    rule_result = check_user_rules(text, user_rules)
    if rule_result["triggered"]:
        return {
            "risk_level": rule_result["override_level"],
            "risk_reason": rule_result["reason"],
            "action": "escalate"
        }

    # --- Intent-based classification ---
    if intent == "promotional":
        return {
            "risk_level": "low",
            "risk_reason": "Promotional email — safe to handle automatically",
            "action": "auto_draft"
        }

    if intent == "casual":
        # Casual emails are low risk unless medium keywords present
        for keyword in MEDIUM_RISK_KEYWORDS:
            if keyword in text:
                return {
                    "risk_level": "medium",
                    "risk_reason": f"Commitment keyword detected: '{keyword}'",
                    "action": "suggest_and_approve"
                }
        return {
            "risk_level": "low",
            "risk_reason": "Casual email with no sensitive keywords",
            "action": "auto_draft"
        }

    if intent == "scheduling":
        # Scheduling always needs approval — we never auto-confirm anything
        return {
            "risk_level": "medium",
            "risk_reason": "Scheduling request — requires user approval before responding",
            "action": "suggest_and_approve"
        }

    if intent == "urgent":
        # Urgent emails always escalate to user
        return {
            "risk_level": "high",
            "risk_reason": "Urgent email — requires immediate user attention",
            "action": "escalate"
        }

    # Default fallback
    return {
        "risk_level": "medium",
        "risk_reason": "Could not determine risk level confidently",
        "action": "suggest_and_approve"
    }