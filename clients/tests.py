from django.contrib.auth.models import User
from django.test import TestCase
from .models import ClientProfile, RiskAssessment


class RiskAssessmentTests(TestCase):
    def test_risk_assessment_calculates_suitable_outcome(self):
        user = User.objects.create_user(username="adviser", password="Test12345!")
        client = ClientProfile.objects.create(full_name="Test Client", email="client@example.com", created_by=user)
        assessment = RiskAssessment.objects.create(client=client, risk_tolerance="BALANCED", risk_capacity="GROWTH", assessed_by=user)
        self.assertEqual(assessment.assessment_score, 7)
        self.assertEqual(assessment.outcome, "SUITABLE")
