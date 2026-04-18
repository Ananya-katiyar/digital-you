import sys
import os
sys.path.insert(0, os.path.abspath("."))

from app.services.nlp import analyse_email

samples = [
    {
        "subject": "Quick catch up?",
        "snippet": "Hey, are you available for a call tomorrow at 3pm?",
        "sender": "john@example.com"
    },
    {
        "subject": "URGENT: Action Required",
        "snippet": "Please respond immediately, this is time sensitive.",
        "sender": "boss@company.com"
    },
    {
        "subject": "50% OFF - Limited Time Offer!",
        "snippet": "Click here to unsubscribe or view our deals.",
        "sender": "noreply@shop.com"
    },
    {
        "subject": "How are you?",
        "snippet": "Just checking in, hope you're doing well.",
        "sender": "friend@gmail.com"
    },
    {
        "subject": "Project meeting next week",
        "snippet": "Can we schedule a sync to discuss the roadmap?",
        "sender": "manager@work.com"
    },
]

for s in samples:
    result = analyse_email(s["subject"], s["snippet"], s["sender"])
    print(f"Subject: {s['subject']}")
    print(f"  Intent:   {result['intent']}")
    print(f"  Entities: {result['entities']}")
    print()