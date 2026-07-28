from django.contrib.auth.models import User
# Imports Django's built-in User model, which is used here to create a test user for the permission test.
from django.test import Client, TestCase
# Imports TestCase for writing database-backed Django tests, and Client for pretending to use the website like a browser.
from clients.models import ClientProfile
# Imports the ClientProfile model from the clients app because a mandate must be connected to a client record.
from .models import InvestmentMandate
# Imports the InvestmentMandate model from the current mandates app so the test can create a mandate in the test database.

class PermissionTests(TestCase):
    # Creates a test class for permission-related tests in the mandates app.
    # TestCase gives Django a temporary test database, so this test does not affect the real Neon database.
    def test_client_role_cannot_approve_mandate(self):
        # This test checks that a normal client user is not allowed to approve an investment mandate.
        # It connects to the wider framework idea of authorization, where not every logged-in user has the same permissions.
        user = User.objects.create_user(username="client", password="Test12345!")
        # Creates a test user with the username "client" and a password.
        # create_user() is better than create() because it hashes the password properly, just like Django does in the real app.
        client_record = ClientProfile.objects.create(full_name="Client", email="client@example.com", created_by=user)
        # Creates a client profile record in the test database.
        # The created_by=user part links this client profile to the user who created it, which reflects the app's client-management workflow.
        mandate = InvestmentMandate.objects.create(client=client_record, mandate_name="Test Mandate", objective="Growth", mandate_type="ADVISORY", created_by=user)
        # Creates a test investment mandate connected to the client profile.
        # This gives the test an actual mandate record to try approving, instead of testing with empty data.
        # The objective is "Growth" and the mandate type is "ADVISORY", which matches the portfolio suitability workflow.
        web = Client()
        # Creates Django's test browser client.
        # This lets the test send requests to URLs in the project without opening a real browser.
        web.login(username="client", password="Test12345!")
        # Logs the test user into the test browser.
        # This is important because the test is checking authorization, not login failure.
        # The user is authenticated, but they still should not be allowed to approve the mandate.
        response = web.get(f"/mandates/{mandate.pk}/approve/")
        # Sends a GET request to the mandate approval URL.
        # mandate.pk inserts the primary key of the test mandate into the URL.
        # This simulates the user trying to access the approval page directly.
        self.assertEqual(response.status_code, 403)
        # Checks that the response status code is 403 Forbidden.
        # 403 means the user is logged in, but Django/the app refuses access because the user does not have permission.
        # This proves that the approval view is protected and that client users cannot approve mandates.