"""Models for user role and personal contact details."""

from django.conf import settings
# This imports the Django settings file, so the model can refer to the active user model safely instead of hardcoding "User".

from django.db import models
# This imports Django's model system, which is used to create database tables through Python classes.

class UserProfile(models.Model):
    # This creates a database model called UserProfile, and because it inherits from models.Model, Django will turn it into a database table.
    """Extends Django's built-in User with role and contact details.
    This supports the assignment requirement for users to update personal/contact
    information and for the application to restrict access by user role.
    """
   

    class Role(models.TextChoices):
        # This inner class defines fixed role options, which helps avoid spelling mistakes when assigning user permissions.

        CLIENT = "CLIENT", "Client"
        # This role is for normal client users; the first value is stored in the database, and the second value is shown nicely on forms/admin.

        ADVISER = "ADVISER", "Adviser"
        # This role represents an adviser user, who would normally create or manage client suitability information.

        PORTFOLIO_MANAGER = "PORTFOLIO_MANAGER", "Portfolio Manager"
        # This role represents a portfolio manager, which is important because this user type can approve mandates later.

        COMPLIANCE = "COMPLIANCE", "Compliance Reviewer"
        # This role represents a compliance reviewer, which connects to the governance and approval side of the application.

        ADMIN = "ADMIN", "Administrator"
        # This role represents an administrator, who has the highest level of access in this role system.

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    # This links each UserProfile to exactly one Django user, creating a one-to-one relationship between the login account and the extra profile details.

    # settings.AUTH_USER_MODEL is used instead of importing User directly because it is the recommended flexible way to reference Django's user model.

    # on_delete=models.CASCADE means if the main user account is deleted, the related profile is also deleted, so there is no orphan profile left behind.

    # related_name="profile" means I can access the profile from a user object using user.profile, which makes the code cleaner in views and templates.

    role = models.CharField(max_length=30, choices=Role.choices, default=Role.CLIENT)
    # This stores the user's role as text in the database, limited to the choices defined in the Role class above.

    # max_length=30 gives enough space for longer role values such as PORTFOLIO_MANAGER.

    # choices=Role.choices means Django will only allow one of the defined roles, which makes the field safer and easier to display in forms.

    # default=Role.CLIENT means every new profile starts as a Client unless another role is selected.

    phone = models.CharField(max_length=40, blank=True)
    # This stores the user's phone number as text because phone numbers may include spaces, plus signs, or country codes.

    # blank=True means the field is optional in Django forms, so the user can save the profile without entering a phone number.

    organisation = models.CharField(max_length=150, blank=True)
    # This stores the organisation or company linked to the user, which supports the assignment requirement for contact/profile details.

    # blank=True makes this field optional, because not every user may belong to an organisation.

    job_title = models.CharField(max_length=120, blank=True)
    # This stores the user's job title, such as Adviser, Analyst, or Compliance Reviewer.

    # This field helps make the profile more realistic for a portfolio suitability review system.

    created_at = models.DateTimeField(auto_now_add=True)
    # This automatically stores the date and time when the profile is first created.

    # auto_now_add=True is useful for audit/history purposes because it records the original creation timestamp only once.

    updated_at = models.DateTimeField(auto_now=True)
    # This automatically updates the date and time every time the profile record is saved.

    # auto_now=True is useful because it shows when the contact or role information was last changed.

    def __str__(self):
        # This method controls how the UserProfile object appears in the Django admin panel and shell.

        return f"{self.user.get_username()} - {self.get_role_display()}"
        # This returns a readable label, showing the username and the human-friendly role name.

        # self.user.get_username() gets the username from the linked Django user account.

        # self.get_role_display() converts the stored role value, such as CLIENT, into the readable label, such as Client.

    @property
    # This decorator lets can_approve_mandates behave like a normal attribute instead of a method call.

    def can_approve_mandates(self):
        # This creates a reusable permission helper that checks whether the user has authority to approve investment mandates.

        return self.role in {self.Role.PORTFOLIO_MANAGER, self.Role.COMPLIANCE, self.Role.ADMIN}
        # This returns True only if the user's role is Portfolio Manager, Compliance Reviewer, or Administrator.

        # This connects the model to the wider framework logic because views/templates can use this property to restrict approval buttons and actions.