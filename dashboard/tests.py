# Import Django's built-in User model, which is the standard model used for creating and managing users in this project.
from django.contrib.auth.models import User
# Import Client and TestCase from Django's testing framework.
# Client lets the test act like a browser, and TestCase gives us a temporary test database for safe testing.
from django.test import Client, TestCase

# This class groups together route/page tests for the dashboard app.
# A test class should inherit from TestCase so Django can set up and clean up a test database automatically.
class RouteTests(TestCase):
    # This test checks that the public home page loads successfully.
    # It is useful because the home page should be accessible even when the user is not logged in.
    def test_public_home_loads(self):
        # Send a GET request to the root URL, just like a browser visiting http://127.0.0.1:8000/.
        # self.client is Django's built-in test browser that comes from TestCase.
        response = self.client.get("/")
        # Check that the page returns HTTP status code 200.
        # Status code 200 means the page loaded successfully.
        self.assertEqual(response.status_code, 200)
        
    # This test checks that the dashboard page is protected.
    # Since the dashboard contains private user/project information, users should not access it unless logged in.
    def test_dashboard_requires_login(self):
        # Send a GET request to the dashboard URL without logging in first.
        # This simulates an anonymous visitor trying to open the dashboard page.
        response = self.client.get("/dashboard/")
        # Check that Django returns HTTP status code 302.
        # Status code 302 means redirect, which usually sends the user to the login page.
        self.assertEqual(response.status_code, 302)
        
    # This test checks that a logged-in user can access the dashboard.
    # It confirms that the login protection works correctly without blocking valid users.
    def test_logged_in_dashboard_loads(self):
        # Create a test user inside the temporary test database.
        # create_user automatically hashes the password, just like Django does in the real application.
        User.objects.create_user(username="tester", password="Test12345!")
        # Create a separate test browser client.
        # This helps simulate a real user session after login.
        web = Client()
        # Log the test user into the test client using the same username and password created above.
        # If the login is successful, future requests from this client act as an authenticated user.
        web.login(username="tester", password="Test12345!")
        # Send a GET request to the dashboard page as the logged-in user.
        # This checks whether authenticated users are allowed to view the dashboard.
        response = web.get("/dashboard/")
        # Check that the dashboard returns HTTP status code 200.
        # Status code 200 means the logged-in user can successfully open the dashboard page.
        self.assertEqual(response.status_code, 200)