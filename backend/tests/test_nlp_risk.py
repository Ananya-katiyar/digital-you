import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.nlp import detect_intent, extract_entities, analyse_email
from app.services.risk import classify_risk, check_user_rules

class TestIntentDetection:

    def test_scheduling_intent(self):
        """Standard scheduling email is detected correctly"""
        result = detect_intent(
            subject="Quick catch up?",
            snippet="Are you available for a call tomorrow at 3pm?",
            sender="john@example.com"
        )
        assert result == "scheduling"

    def test_urgent_intent(self):
        """Urgent email is detected correctly"""
        result = detect_intent(
            subject="URGENT: Action Required",
            snippet="Please respond immediately, this is time sensitive.",
            sender="boss@company.com"
        )
        assert result == "urgent"

    def test_promotional_intent(self):
        """Promotional email is detected correctly"""
        result = detect_intent(
            subject="50% OFF Sale!",
            snippet="Click here to unsubscribe from our newsletter.",
            sender="noreply@shop.com"
        )
        assert result == "promotional"

    def test_casual_intent(self):
        """Casual email defaults correctly"""
        result = detect_intent(
            subject="How are you?",
            snippet="Just checking in, hope you are doing well.",
            sender="friend@gmail.com"
        )
        assert result == "casual"

    def test_free_word_not_promotional(self):
        """
        Edge case: 'free' in 'I am free Monday' must NOT
        trigger promotional intent — this was our Day 9 bug
        """
        result = detect_intent(
            subject="Project meeting next week",
            snippet="I am free Monday or Tuesday, let me know.",
            sender="manager@work.com"
        )
        assert result == "scheduling"

    def test_promotional_beats_scheduling(self):
        """
        Promotional is checked first — an email with both
        scheduling and promo keywords should be promotional
        """
        result = detect_intent(
            subject="Book your free trial now",
            snippet="Schedule a demo and unsubscribe anytime.",
            sender="noreply@saas.com"
        )
        assert result == "promotional"

    def test_sender_noreply_is_promotional(self):
        """noreply sender pattern alone should trigger promotional"""
        result = detect_intent(
            subject="Your weekly update",
            snippet="Here is your summary for this week.",
            sender="noreply@service.com"
        )
        assert result == "promotional"

class TestRiskClassification:

    def test_promotional_is_low_risk(self):
        """Promotional emails are always low risk"""
        result = classify_risk(
            subject="Sale today!",
            snippet="Unsubscribe from our newsletter.",
            intent="promotional",
            entities=[]
        )
        assert result["risk_level"] == "low"
        assert result["action"] == "auto_draft"

    def test_casual_is_low_risk(self):
        """Casual emails with no sensitive keywords are low risk"""
        result = classify_risk(
            subject="How are you?",
            snippet="Just checking in, hope you are well.",
            intent="casual",
            entities=[]
        )
        assert result["risk_level"] == "low"
        assert result["action"] == "auto_draft"

    def test_scheduling_is_medium_risk(self):
        """Scheduling emails always require approval"""
        result = classify_risk(
            subject="Call tomorrow?",
            snippet="Are you free for a call at 3pm?",
            intent="scheduling",
            entities=[]
        )
        assert result["risk_level"] == "medium"
        assert result["action"] == "suggest_and_approve"

    def test_urgent_is_high_risk(self):
        """Urgent emails always escalate"""
        result = classify_risk(
            subject="URGENT",
            snippet="Please respond immediately.",
            intent="urgent",
            entities=[]
        )
        assert result["risk_level"] == "high"
        assert result["action"] == "escalate"

    def test_salary_keyword_is_high_risk(self):
        """
        Edge case: salary keyword overrides scheduling intent.
        Even if the email looks like a meeting request,
        financial keywords must escalate.
        """
        result = classify_risk(
            subject="Salary discussion",
            snippet="I wanted to discuss your compensation and budget.",
            intent="scheduling",
            entities=[]
        )
        assert result["risk_level"] == "high"
        assert result["action"] == "escalate"

    def test_password_keyword_is_high_risk(self):
        """Security keywords always escalate regardless of intent"""
        result = classify_risk(
            subject="Your account password",
            snippet="Here is your OTP and verification code.",
            intent="casual",
            entities=[]
        )
        assert result["risk_level"] == "high"
        assert result["action"] == "escalate"

    def test_legal_keyword_is_high_risk(self):
        """Legal keywords always escalate"""
        result = classify_risk(
            subject="Contract review",
            snippet="Please review the attached legal document and sign.",
            intent="casual",
            entities=[]
        )
        assert result["risk_level"] == "high"
        assert result["action"] == "escalate"

    def test_commitment_keyword_upgrades_casual_to_medium(self):
        """
        Edge case: casual email with a commitment keyword
        should upgrade to medium risk
        """
        result = classify_risk(
            subject="Quick question",
            snippet="Can you confirm and approve the proposal by Friday?",
            intent="casual",
            entities=[]
        )
        assert result["risk_level"] == "medium"
        assert result["action"] == "suggest_and_approve"

class TestUserRuleEngine:

    def test_hr_rule_triggers_on_hr_content(self):
        """User rule 'escalate HR topics' fires on HR email"""
        rules = [
            {
                "description": "Escalate HR topics",
                "rule_type": "topic_based",
                "condition": "hr_topics",
                "action": "escalate"
            }
        ]
        result = check_user_rules(
            text="resignation letter submitted to human resources",
            rules=rules
        )
        assert result["triggered"] == True
        assert result["override_level"] == "high"

    def test_after_6pm_rule_triggers_at_night(self):
        """Time rule fires correctly when hour >= 18"""
        rules = [
            {
                "description": "Don't schedule after 6 PM",
                "rule_type": "time_based",
                "condition": "after_6pm",
                "action": "escalate"
            }
        ]
        result = check_user_rules(
            text="can we schedule a meeting tomorrow",
            rules=rules,
            current_hour=19
        )
        assert result["triggered"] == True

    def test_after_6pm_rule_does_not_trigger_during_day(self):
        """Time rule must NOT fire during business hours"""
        rules = [
            {
                "description": "Don't schedule after 6 PM",
                "rule_type": "time_based",
                "condition": "after_6pm",
                "action": "escalate"
            }
        ]
        result = check_user_rules(
            text="can we schedule a meeting tomorrow",
            rules=rules,
            current_hour=14
        )
        assert result["triggered"] == False

    def test_no_rules_never_triggers(self):
        """Empty rules list should never trigger"""
        result = check_user_rules(
            text="salary payment invoice legal contract",
            rules=[]
        )
        assert result["triggered"] == False