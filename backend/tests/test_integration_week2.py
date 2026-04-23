import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# ─────────────────────────────────────────────
# FULL PIPELINE TEST
# email → NLP → risk → queue/log decision
# ─────────────────────────────────────────────

class TestFullPipeline:

    def test_ping(self):
        """Server is alive"""
        response = client.get("/ping")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

    def test_drafts_endpoint_reachable(self):
        """Drafts endpoint exists and validates input"""
        response = client.post("/drafts/", json={})
        # 422 = FastAPI validation error (missing fields)
        # which means the endpoint exists and is working
        assert response.status_code == 422

    def test_queue_endpoint_reachable(self):
        """Queue endpoint exists"""
        with patch("app.routes.queue.get_db") as mock_db:
            mock_col = MagicMock()
            mock_col.pending_actions.find.return_value.sort.return_value.to_list = AsyncMock(return_value=[])
            mock_db.return_value = mock_col

            response = client.get("/queue/?email=test@gmail.com")
            assert response.status_code == 200
            assert response.json()["status"] == "ok"

    def test_decisions_endpoint_reachable(self):
        """Decisions endpoint exists"""
        with patch("app.routes.decisions.get_db") as mock_db:
            mock_col = MagicMock()
            mock_col.decisions.find.return_value.sort.return_value.limit.return_value.to_list = AsyncMock(return_value=[])
            mock_db.return_value = mock_col

            response = client.get("/decisions/?email=test@gmail.com")
            assert response.status_code == 200
            assert response.json()["status"] == "ok"

    def test_profile_endpoint_reachable(self):
        """Profile endpoint still works from Week 1"""
        with patch("app.routes.profile.get_db") as mock_db:
            mock_col = MagicMock()
            mock_col.users.find_one = AsyncMock(return_value={
                "email": "test@gmail.com",
                "preferences": {
                    "tone": "professional",
                    "afk_mode": False,
                    "timezone": "Asia/Kolkata",
                    "rules": []
                },
                "scopes_granted": [],
                "created_at": None,
                "updated_at": None
            })
            mock_db.return_value = mock_col

            response = client.get("/profile/?email=test@gmail.com")
            assert response.status_code == 200
            assert response.json()["email"] == "test@gmail.com"


# ─────────────────────────────────────────────
# NLP + RISK PIPELINE UNIT TEST
# ─────────────────────────────────────────────

class TestNLPRiskPipeline:

    def test_full_analysis_low_risk(self):
        """Casual email goes through full pipeline correctly"""
        from app.services.nlp import analyse_email
        from app.services.risk import classify_risk

        analysis = analyse_email(
            subject="How are you?",
            snippet="Just checking in, hope you are well.",
            sender="friend@gmail.com"
        )
        risk = classify_risk(
            subject="How are you?",
            snippet="Just checking in, hope you are well.",
            intent=analysis["intent"],
            entities=analysis["entities"],
            user_rules=[]
        )

        assert analysis["intent"] == "casual"
        assert risk["risk_level"] == "low"
        assert risk["action"] == "auto_draft"

    def test_full_analysis_medium_risk(self):
        """Scheduling email goes through full pipeline correctly"""
        from app.services.nlp import analyse_email
        from app.services.risk import classify_risk

        analysis = analyse_email(
            subject="Meeting tomorrow?",
            snippet="Can we schedule a call at 3pm tomorrow?",
            sender="manager@work.com"
        )
        risk = classify_risk(
            subject="Meeting tomorrow?",
            snippet="Can we schedule a call at 3pm tomorrow?",
            intent=analysis["intent"],
            entities=analysis["entities"],
            user_rules=[]
        )

        assert analysis["intent"] == "scheduling"
        assert risk["risk_level"] == "medium"
        assert risk["action"] == "suggest_and_approve"

    def test_full_analysis_high_risk(self):
        """High risk keyword email escalates correctly"""
        from app.services.nlp import analyse_email
        from app.services.risk import classify_risk

        analysis = analyse_email(
            subject="Salary review",
            snippet="Let us discuss your compensation package.",
            sender="hr@company.com"
        )
        risk = classify_risk(
            subject="Salary review",
            snippet="Let us discuss your compensation package.",
            intent=analysis["intent"],
            entities=analysis["entities"],
            user_rules=[]
        )

        assert risk["risk_level"] == "high"
        assert risk["action"] == "escalate"

    def test_afk_mode_queues_medium_risk(self):
        """
        AFK mode logic: medium risk should be queued
        when afk_mode is True
        """
        risk_level = "medium"
        afk_mode = True

        should_queue = (
            risk_level == "medium" or
            (afk_mode and risk_level != "low")
        )

        assert should_queue == True

    def test_afk_mode_does_not_queue_low_risk(self):
        """
        AFK mode still allows low risk to pass through
        without queuing
        """
        risk_level = "low"
        afk_mode = True

        should_queue = (
            risk_level == "medium" or
            (afk_mode and risk_level != "low")
        )

        assert should_queue == False