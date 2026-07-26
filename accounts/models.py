"""Models for user role and personal contact details."""
from django.conf import settings
# This imports the Django settings, which lets this model safely refer to the active user model used by the whole project.
from django.db import models
# This imports Django's model tools, which are used to create database tables by writing Python classes instead of raw SQL.


class UserProfile(models.Model):
    # This creates a Django model called UserProfile, and Django will convert this class into a database table when migrations are run.
    """Extends Django's built-in User with role and contact details. This supports the assignment requirement for users to update personal/contact
    information and for the application to restrict access by user role."""

    class Role(models.TextChoices):
        # This inner class creates a fixed list of allowed user roles, so the project does not rely on random typed text values.
        CLIENT = "CLIENT", "Client"
        # This role is for a normal client user; "CLIENT" is stored in the database, while "Client" is displayed in forms and the admin panel.
        ADVISER = "ADVISER", "Adviser"
        # This role is for adviser users, who would normally create client records, suitability information, and investment mandates.
        PORTFOLIO_MANAGER = "PORTFOLIO_MANAGER", "Portfolio Manager"
        # This role is for portfolio manager users, which matters because this type of user can be allowed to review or approve mandates.
        COMPLIANCE = "COMPLIANCE", "Compliance Reviewer"
        # This role is for compliance users, which connects the application to governance, checking, and approval responsibilities.
        ADMIN = "ADMIN", "Administrator"
        # This role is for administrator users, who represent the highest access level in this custom role system.

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    # This creates a one-to-one database relationship between the built-in Django user account and this extra profile record.
    # A OneToOneField means each login user has one profile, and each profile belongs to only one login user.
    # settings.AUTH_USER_MODEL is used instead of importing User directly because it follows Django best practice and keeps the project flexible.
    # on_delete=models.CASCADE means if the user account is deleted, the matching profile is deleted too, which avoids leaving unused profile records.
    # related_name="profile" lets the project access this profile using user.profile in views, templates, and permission checks.
    role = models.CharField(max_length=30, choices=Role.choices, default=Role.CLIENT)
    # This stores the user's role as text in the database.
    # max_length=30 gives enough space for longer role names such as PORTFOLIO_MANAGER.
    # choices=Role.choices means Django will restrict this field to the role options defined above, which helps prevent inconsistent data.
    # default=Role.CLIENT means every new profile starts as a Client unless the system or admin changes the role.
    # This field connects directly to the wider permission logic because the user's role controls what actions they can perform.
    phone = models.CharField(max_length=40, blank=True)
    # This stores the user's phone number as text rather than a number because phone numbers can include spaces, plus signs, and country codes.
    # blank=True means the field is optional in Django forms, so users can update their profile without being forced to enter a phone number.
    organisation = models.CharField(max_length=150, blank=True)
    # This stores the user's organisation or company name, which makes the profile more realistic for a professional portfolio review system.
    # blank=True means the organisation field is optional because some users may not belong to a company or may not want to provide it.
    job_title = models.CharField(max_length=120, blank=True)
    # This stores the user's job title, such as Adviser, Analyst, Portfolio Manager, or Compliance Reviewer.
    # This field supports the wider application context by making user profiles look more like real workplace records.
    created_at = models.DateTimeField(auto_now_add=True)
    # This automatically saves the date and time when the profile is first created.
    # auto_now_add=True only sets the timestamp once, which is useful for basic audit history and record tracking.
    updated_at = models.DateTimeField(auto_now=True)
    # This automatically updates the date and time every time the profile is saved.
    # auto_now=True helps show when the profile information was last changed, which is useful for contact and governance records.

    def __str__(self):
        # This method controls how the UserProfile object appears as text in the Django admin panel, shell, and debugging output.
        return f"{self.user.get_username()} - {self.get_role_display()}"
        # This returns a clear label made from the linked username and the readable role name.
        # self.user.get_username() gets the username from the connected Django user account.
        # self.get_role_display() converts the stored database value, such as CLIENT, into the human-friendly label, such as Client.
        # This makes admin records easier to understand because the profile is shown as a useful name instead of just "UserProfile object".

    @property
    # This decorator lets can_approve_mandates be used like an attribute, for example user.profile.can_approve_mandates, instead of calling it like a method.
    def can_approve_mandates(self):
        # This creates a reusable permission helper for checking whether this user profile can approve investment mandates.
        # Keeping this logic in the model helps avoid repeating the same role-checking code across different views and templates.
        return self.role in {self.Role.PORTFOLIO_MANAGER, self.Role.COMPLIANCE, self.Role.ADMIN}
        # This returns True only when the user's role is Portfolio Manager, Compliance Reviewer, or Administrator.
        # It returns False for Client and Adviser users because those roles should not approve mandates in this workflow.
        # This connects the accounts app to the mandates app because mandate approval depends on the role stored here.
        # Views can use this property to block unauthorised approval actions, while templates can use it to show or hide approval buttons.