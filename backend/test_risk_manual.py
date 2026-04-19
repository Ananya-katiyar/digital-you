import sys, os
sys.path.insert(0, os.path.abspath("."))

from app.services.nlp import analyse_email
from app.services.risk import classify_risk

samples = [
    {
        "subject": "50% OFF Sale!",
        "snippet": "Click here to unsubscribe from our newsletter.",
        "sender": "noreply@shop.com"
    },
    {
        "subject": "Quick catch up?",
        "snippet": "Are you free for a call tomorrow at 3pm?",
        "sender": "john@example.com"
    },
    {
        "subject": "URGENT: Action Required",
        "snippet": "Please respond immediately, this is critical.",
        "sender": "boss@company.com"
    },
    {
        "subject": "Salary discussion",
        "snippet": "I wanted to discuss your compensation and budget for next year.",
        "sender": "hr@company.com"
    },
    {
        "subject": "Your account password",
        "snippet": "Here is your OTP and verification code to access your account.",
        "sender": "security@bank.com"
    },
    {
        "subject": "How are you?",
        "snippet": "Just checking in, hope you're doing well!",
        "sender": "friend@gmail.com"
    },
]

# Test with a user rule
user_rules = ["escalate HR topics", "don't schedule after 6 PM"]

for s in samples:
    analysis = analyse_email(s["subject"], s["snippet"], s["sender"])
    risk = classify_risk(
        subject=s["subject"],
        snippet=s["snippet"],
        intent=analysis["intent"],
        entities=analysis["entities"],
        user_rules=user_rules
    )
    print(f"Subject : {s['subject']}")
    print(f"Intent  : {analysis['intent']}")
    print(f"Risk    : {risk['risk_level'].upper()} — {risk['risk_reason']}")
    print(f"Action  : {risk['action']}")
    print()