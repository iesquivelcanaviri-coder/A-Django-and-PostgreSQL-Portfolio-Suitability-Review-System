from django.contrib.auth.models import User
from django.test import Client, TestCase
from clients.models import ClientProfile
from .models import InvestmentMandate


class PermissionTests(TestCase):
    def test_client_role_cannot_approve_mandate(self):
        user = User.objects.create_user(username="client", password="Test12345!")
        client_record = ClientProfile.objects.create(full_name="Client", email="client@example.com", created_by=user)
        mandate = InvestmentMandate.objects.create(client=client_record, mandate_name="Test Mandate", objective="Growth", mandate_type="ADVISORY", created_by=user)
        web = Client()
        web.login(username="client", password="Test12345!")
        response = web.get(f"/mandates/{mandate.pk}/approve/")
        self.assertEqual(response.status_code, 403)
