from django.contrib.auth.models import User
from django.test import Client, TestCase


class RouteTests(TestCase):
    def test_public_home_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_dashboard_requires_login(self):
        response = self.client.get("/dashboard/")
        self.assertEqual(response.status_code, 302)

    def test_logged_in_dashboard_loads(self):
        User.objects.create_user(username="tester", password="Test12345!")
        web = Client()
        web.login(username="tester", password="Test12345!")
        response = web.get("/dashboard/")
        self.assertEqual(response.status_code, 200)
