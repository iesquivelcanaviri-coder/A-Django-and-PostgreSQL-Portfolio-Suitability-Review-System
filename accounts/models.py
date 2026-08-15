"""Models for user role and personal contact details."""

from django.conf import settings
# This imports the Django settings, which lets this model safely refer to the active user model used by the whole project.

from django.db import models
# This imports Django's model tools, which are used to create database tables by writing Python classes instead of raw SQL.

from django.db.models.signals import post_save
# This imports Django's post_save signal, which can run code automatically after a user is created or updated.

from django.dispatch import receiver
# This imports receiver, which connects a signal to a function.


class UserProfile(models.Model):
    # This creates a Django model called UserProfile.
    # Django converts this class into a database table when migrations are created and applied.

    """Extends Django's built-in User with role and contact details.

    This supports the assignment requirement for users to update personal/contact
    information and for the application to restrict access by user role.
    """

    class Role(models.TextChoices):
        # This inner class creates a fixed list of allowed user roles.
        # This prevents the project from relying on inconsistent typed text values.

        CLIENT = "CLIENT", "Client"
        # This role is for a normal client user.

        ADVISER = "ADVISER", "Adviser"
        # This role is for adviser users who may help create client records and suitability information.

        PORTFOLIO_MANAGER = "PORTFOLIO_MANAGER", "Portfolio Manager"
        # This role is for portfolio manager users who may be allowed to review or approve mandates.

        COMPLIANCE = "COMPLIANCE", "Compliance Reviewer"
        # This role is for compliance users, supporting governance, checking, and approval responsibilities.

        ADMIN = "ADMIN", "Administrator"
        # This role is for administrator users, representing the highest access level in the custom role system.

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    # This creates a one-to-one database relationship between the built-in Django user account and this extra profile record.
    # Each user has one profile, and each profile belongs to only one user.
    # settings.AUTH_USER_MODEL is used instead of importing User directly because it follows Django best practice.
    # on_delete=models.CASCADE means if the user account is deleted, the matching profile is deleted too.
    # related_name="profile" lets the project access the profile using user.profile.

    role = models.CharField(
        max_length=30,
        choices=Role.choices,
        default=Role.CLIENT,
    )
    # This stores the user's role as text in the database.
    # choices=Role.choices restricts the field to the role options defined above.
    # default=Role.CLIENT means every new profile starts as a Client unless changed by an admin or view.

    phone = models.CharField(max_length=40, blank=True)
    # This stores the user's phone number as text because phone numbers can include spaces, plus signs, and country codes.
    # blank=True makes the field optional in forms.

    organisation = models.CharField(max_length=150, blank=True)
    # This stores the user's organisation or company name.
    # It is optional because not every user needs to provide an organisation.

    job_title = models.CharField(max_length=120, blank=True)
    # This stores the user's job title, such as Adviser, Analyst, Portfolio Manager, or Compliance Reviewer.

    created_at = models.DateTimeField(auto_now_add=True)
    # This automatically saves the date and time when the profile is first created.

    updated_at = models.DateTimeField(auto_now=True)
    # This automatically updates the date and time every time the profile is saved.

    def __str__(self):
        # This method controls how the UserProfile object appears as text in the Django admin panel and shell.

        return f"{self.user.get_username()} - {self.get_role_display()}"
        # This returns a clear label made from the linked username and readable role name.

    @property
    def can_approve_mandates(self):
        # This creates a reusable permission helper for checking whether this user can approve investment mandates.
        # Views and templates can use user.profile.can_approve_mandates instead of repeating role-checking code.

        return self.role in {
            self.Role.PORTFOLIO_MANAGER,
            self.Role.COMPLIANCE,
            self.Role.ADMIN,
        }
        # This returns True only for Portfolio Manager, Compliance Reviewer, or Administrator users.


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    # This function runs automatically whenever a Django user is saved.
    # It makes sure every user has a matching UserProfile record.

    if created:
        # This runs only when a new user account is created.

        UserProfile.objects.create(user=instance)
        # This creates a matching profile for the new user.

    else:
        # This runs when an existing user account is updated.

        UserProfile.objects.get_or_create(user=instance)
        # This safely creates a profile if the existing user does not already have one.
        # This helps prevent errors when old users were created before the profile system existed.