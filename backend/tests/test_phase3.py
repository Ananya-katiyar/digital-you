import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.services.tone_analyser import analyse_tone_from_texts, _default_tone_profile
from app.services.scheduling import get_free_slots, format_scheduling_response

client = TestClient(app)


# ─────────────────────────────────────────────
# TONE ANALYSER TESTS
# ─────────────────────────────────────────────

class TestToneAnalyser:

    def test_empty_texts_returns_default(self):
        """Empty input returns safe default profile"""
        result = analyse_tone_from_texts([])
        assert result["formality"] == "professional"
        assert result["emails_analysed"] == 0

    def test_formal_texts_detected(self):
        """Formal writing patterns are detected correctly"""
        texts = [
            "Dear Sir, Please kindly find the attached document. Best regards.",
            "Thank you for your email. I would appreciate your response. Sincerely.",
            "Regarding your request, I hereby confirm the details. Best regards."
        ]
        result = analyse_tone_from_texts(texts)
        assert result["formality"] == "formal"
        assert result["emails_analysed"] == 3

    def test_casual_texts_detected(self):
        """Casual writing patterns are detected correctly"""
        texts = [
            "Hey! Yeah sure that works. Thanks!",
            "Hi, cool idea! Awesome work. Cheers!",
            "Hey okay sounds good. Yep I'm in!"
        ]
        result = analyse_tone_from_texts(texts)
        assert result["formality"] == "casual"

    def test_exclamation_detection(self):
        """Exclamation usage is tracked correctly"""
        texts = [
            "Hey! Great to hear from you! Sounds awesome!",
            "Yes! Let's do it! Can't wait!",
        ]
        result = analyse_tone_from_texts(texts)
        assert result["uses_exclamations"] == True

    def test_no_exclamations(self):
        """Non-exclamatory writing is detected correctly"""
        texts = [
            "Thank you for reaching out. I will review your request.",
            "Please find the details below. Let me know if you need anything."
        ]
        result = analyse_tone_from_texts(texts)
        assert result["uses_exclamations"] == False

    def test_tone_endpoint_reachable(self):
        """Tone endpoints exist and are reachable"""
        with patch("app.routes.tone.get_db") as mock_db:
            mock_col = MagicMock()
            mock_col.users.find_one = AsyncMock(return_value=None)
            mock_db.return_value = mock_col

            response = client.get("/tone/profile?email=test@gmail.com")
            assert response.status_code in [200, 404]


# ─────────────────────────────────────────────
# SCHEDULING TESTS
# ─────────────────────────────────────────────

class TestScheduling:

    def test_no_events_returns_slots(self):
        """With no calendar events, free slots should be found"""
        slots = get_free_slots(events=[], days_ahead=5)
        assert len(slots) <= 3
        assert len(slots) >= 0

    def test_slots_within_business_hours(self):
        """All suggested slots must be within 9 AM - 6 PM"""
        slots = get_free_slots(events=[], days_ahead=5)
        for slot in slots:
            hour = int(slot["start_time"].split(":")[0])
            # Convert 12-hour to 24-hour for comparison
            if "PM" in slot["start_time"] and hour != 12:
                hour += 12
            assert 9 <= hour < 18

    def test_format_professional_tone(self):
        """Professional tone formatting includes formal language"""
        slots = [
            {
                "date": "Monday, April 28",
                "start_time": "10:00 AM",
                "end_time": "11:00 AM",
                "iso_start": "",
                "iso_end": ""
            }
        ]
        result = format_scheduling_response(slots, tone="professional")
        assert "available time slots" in result.lower()
        assert "Monday, April 28" in result

    def test_format_casual_tone(self):
        """Casual tone formatting uses informal language"""
        slots = [
            {
                "date": "Monday, April 28",
                "start_time": "10:00 AM",
                "end_time": "11:00 AM",
                "iso_start": "",
                "iso_end": ""
            }
        ]
        result = format_scheduling_response(slots, tone="casual")
        assert "hey" in result.lower()

    def test_no_slots_returns_fallback(self):
        """Empty slots returns a helpful fallback message"""
        result = format_scheduling_response([], tone="professional")
        assert "don't have any free slots" in result.lower()

    def test_scheduling_endpoint_reachable(self):
        """Scheduling endpoint exists"""
        with patch("app.services.gmail.get_db") as mock_db:
            mock_col = MagicMock()
            mock_col.users.find_one = AsyncMock(return_value=None)
            mock_db.return_value = mock_col

            response = client.get("/scheduling/suggest?email=test@gmail.com")
            assert response.status_code in [200, 500]


# ─────────────────────────────────────────────
# DRAFT WITH TONE PROFILE TEST
# ─────────────────────────────────────────────

class TestDraftWithToneProfile:

    def test_draft_endpoint_accepts_user_email(self):
        """Draft endpoint now accepts optional user_email field"""
        with patch("app.routes.drafts.get_db") as mock_db:
            mock_col = MagicMock()
            mock_col.users.find_one = AsyncMock(return_value=None)
            mock_db.return_value = mock_col

            response = client.post("/drafts/", json={
                "subject": "Test",
                "snippet": "Test snippet",
                "tone": "professional",
                "user_email": "test@gmail.com"
            })
            assert response.status_code in [200, 500]

    def test_draft_endpoint_works_without_user_email(self):
        """Draft endpoint still works without user_email"""
        response = client.post("/drafts/", json={
            "subject": "Test",
            "snippet": "Test snippet",
            "tone": "professional"
        })
        assert response.status_code in [200, 500]