"""Signals that automatically create a UserProfile for every new user."""
from django.conf import settings
# This imports the main Django settings, which lets me safely refer to the user model used by the project.
# I use settings.AUTH_USER_MODEL instead of importing User directly because it is more flexible and follows Django best practice.
# This means the signal would still work even if the project later changed from Django's default User model to a custom user model.
from django.db.models.signals import post_save
# This imports Django's post_save signal.
# A signal is like an automatic notification inside Django.
# post_save means Django sends this signal after a model object has been saved to the database.
# In this project, I use it to react immediately after a new user account is created.
from django.dispatch import receiver
# This imports the receiver decorator.
# The receiver decorator connects a normal Python function to a Django signal.
# In simple terms, it tells Django: when this signal happens, run this function.
from .models import UserProfile
# This imports the UserProfile model from the current accounts app.
# UserProfile stores extra information that Django's built-in User model does not store, such as role, phone, organisation and job title.
# This keeps authentication details separate from profile and role details, which makes the app cleaner and more modular.

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
# This connects the function below to Django's post_save signal.
# The sender is settings.AUTH_USER_MODEL, so this function runs whenever a user account is saved.
# This is important because user registration happens through Django's authentication system, not directly through the UserProfile model.
# Using this decorator means I do not need to manually create a profile inside every registration view.
def create_user_profile(sender, instance, created, **kwargs):
    # This function runs automatically after a user object is saved.
    # sender is the model that sent the signal, which is the configured User model in this project.
    # instance is the actual user account object that has just been saved.
    # created is True only when the user has been created for the first time.
    # created is False when an existing user is only being updated.
    # **kwargs collects any extra signal information Django sends, so the function stays compatible with Django's signal system.
    """Create a role/contact profile whenever a new Django user is registered."""
    if created:
        # This checks whether the user account is brand new.
        # I only want to create a UserProfile when the user is first registered.
        # Without this condition, Django could try to create another profile every time the user is saved or updated.
        # That would be a problem because the relationship should be one user to one profile.
        UserProfile.objects.create(user=instance)
        # This creates a new UserProfile record in the database.
        # user=instance links the new profile to the exact user account that triggered the signal.
        # This connection supports the wider framework design of the project:
        # Django's built-in User model handles login, password and authentication.
        # My UserProfile model handles extra project-specific information such as user role and contact details.
        # This is useful for the assignment because it shows model relationships, automatic database actions and role-based access.