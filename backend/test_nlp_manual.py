import sys
import os
sys.path.insert(0, os.path.abspath("."))

from app.services.nlp import analyse_email

samples = [
    {
        "subject": "Quick catch up?",
        "snippet": "Hey, are you available for a call tomorrow at 3pm? I wanted to discuss the project timeline and next steps with the team.",
        "sender": "john@example.com"
    },
    {
        "subject": "URGENT: Action Required",
        "snippet": "Please respond immediately. The deadline is by end of day. This is time sensitive and critical.",
        "sender": "boss@company.com"
    },
    {
        "subject": "50% OFF - Limited Time Offer!",
        "snippet": "Click here to unsubscribe or view our latest deals. Limited time only. Free shipping on all orders.",
        "sender": "noreply@shop.com"
    },
    {
        "subject": "How are you doing?",
        "snippet": "Just checking in, hope you are doing well. Let me know if you want to grab coffee sometime.",
        "sender": "friend@gmail.com"
    },
    {
        "subject": "Project meeting next week",
        "snippet": "Can we schedule a sync to discuss the roadmap? I am free Monday or Tuesday. Let me know what works for you.",
        "sender": "manager@work.com"
    },
]

for s in samples:
    result = analyse_email(s["subject"], s["snippet"], s["sender"])
    print(f"Subject  : {s['subject']}")
    print(f"Intent   : {result['intent']}")
    print(f"Entities : {result['entities']}")
    print(f"Summary  : {result['summary']}")
    print()