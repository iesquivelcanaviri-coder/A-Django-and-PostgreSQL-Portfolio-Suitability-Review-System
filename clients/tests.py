from django.contrib.auth.models import User
# Imports Django's built-in User model, which is used here to create a test adviser account for the assessment.
from django.test import TestCase
# Imports Django's TestCase class, which gives us a safe test database that is created and destroyed during testing.
from .models import ClientProfile, RiskAssessment
# Imports the ClientProfile and RiskAssessment models from the current clients app so we can test how they work together.

class RiskAssessmentTests(TestCase):
    # This class groups tests related to the RiskAssessment model, which keeps the testing file organised and easier to read.
    def test_risk_assessment_calculates_suitable_outcome(self):
        # This test checks that a risk assessment is saved correctly and that the model calculates the expected score and outcome.
        user = User.objects.create_user(username="adviser", password="Test12345!")
        # Creates a test user using Django's built-in authentication system.
        # I need a user because the ClientProfile and RiskAssessment records are linked to the person who created or assessed them.
        # In the wider framework, this connects the clients app to Django's auth system and supports the role-based workflow.
        client = ClientProfile.objects.create(full_name="Test Client", email="client@example.com", created_by=user)
        # Creates a test client profile in the temporary test database.
        # The client is given a name, email address, and a created_by user so the record has the same structure as a real client record.
        # This helps test the "know your client" part of the application workflow.
        assessment = RiskAssessment.objects.create(client=client, risk_tolerance="BALANCED", risk_capacity="GROWTH", assessed_by=user)
        # Creates a risk assessment linked to the test client and the test adviser.
        # The values BALANCED and GROWTH are used because the model should convert these choices into a suitability score.
        # This checks that the business logic in the model works, not just that the page loads.
        self.assertEqual(assessment.assessment_score, 7)
        # Checks that the model calculated the expected assessment score.
        # If the model logic changes or breaks, this test will fail and show that the suitability calculation needs checking.
        self.assertEqual(assessment.outcome, "SUITABLE")
        # Checks that the final outcome is SUITABLE based on the calculated score.
        # This confirms that the risk assessment workflow produces the correct result for this test case.