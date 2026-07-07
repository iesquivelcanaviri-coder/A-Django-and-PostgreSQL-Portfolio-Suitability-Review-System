"""Models for user role and personal contact details."""
from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    """Extends Django's built-in User with role and contact details.

    This supports the assignment requirement for users to update personal/contact
    information and for the application to restrict access by user role.
    """

    class Role(models.TextChoices):
        CLIENT = "CLIENT", "Client"
        ADVISER = "ADVISER", "Adviser"
        PORTFOLIO_MANAGER = "PORTFOLIO_MANAGER", "Portfolio Manager"
        COMPLIANCE = "COMPLIANCE", "Compliance Reviewer"
        ADMIN = "ADMIN", "Administrator"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=30, choices=Role.choices, default=Role.CLIENT)
    phone = models.CharField(max_length=40, blank=True)
    organisation = models.CharField(max_length=150, blank=True)
    job_title = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_username()} - {self.get_role_display()}"

    @property
    def can_approve_mandates(self):
        return self.role in {self.Role.PORTFOLIO_MANAGER, self.Role.COMPLIANCE, self.Role.ADMIN}
