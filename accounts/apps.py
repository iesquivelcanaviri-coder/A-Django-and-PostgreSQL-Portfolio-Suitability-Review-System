# ==========================================================
# ACCOUNTS APP CONFIGURATION
# ==========================================================
# This file belongs to the accounts app.
# Django uses apps.py to understand how this app should be loaded inside the wider project.
# In this project, the accounts app is responsible for user profiles, roles and account-related logic.

# This imports AppConfig from Django.
# AppConfig is the base class Django provides for configuring an individual app.
# By inheriting from AppConfig, I can tell Django important details about this app,
# such as its name and what should happen when the app is ready.
from django.apps import AppConfig


# This creates the configuration class for the accounts app.
# Django will use this class when the app is added to INSTALLED_APPS in settings.py.
# The class name normally follows the app name, so accounts becomes AccountsConfig.
class AccountsConfig(AppConfig):
    # This tells Django what type of automatic primary key field to use for models in this app.
    # A primary key is the unique ID Django gives to each record in a database table.
    # For example, each UserProfile record will need its own unique ID.
    # BigAutoField creates a large integer ID automatically, such as 1, 2, 3 and so on.
    # Django recommends BigAutoField for newer projects because it can support many records.
    # This connects to the database layer because Django will use this setting when creating tables
    # through migrations.
    default_auto_field = "django.db.models.BigAutoField"
    # This tells Django the name of the app folder.
    # The value must match the actual folder name, which is accounts.
    # Django uses this name to locate the app's models, views, forms, admin settings and signals.
    # This is also how the app connects to the wider project through INSTALLED_APPS in settings.py.
    # Example in settings.py:
    # INSTALLED_APPS = [
    #     "accounts.apps.AccountsConfig",
    # ]
    # Using the full config path is useful because it allows Django to run the ready() method below.
    name = "accounts"

    # The ready() method runs when Django has finished loading this app.
    # I am using ready() to import the signals file when the project starts.
    # This is important because signals only work if Django has loaded the file where they are defined.
    def ready(self):
        # This imports the accounts.signals file.
        # Even though the import looks unused, it is important because importing the file registers
        # the signal functions with Django.
        # In this project, the signals file can automatically create or update a UserProfile
        # when a built-in Django User is created or saved.
        # Wider framework connection:
        # - Django's built-in User model stores login details such as username, email and password.
        # - The UserProfile model stores extra project-specific details such as role, phone,
        #   organisation and job title.
        # - Signals connect these two models automatically.
        # This helps avoid repeating profile-creation code inside every registration view.
        # For example, when a new user registers, Django can automatically create the matching
        # UserProfile in the background.
        # The noqa: F401 comment tells code checkers not to warn that this import is unused.
        # It may look unused in this file, but it is actually needed because the act of importing
        # accounts.signals activates the signal handlers.
        import accounts.signals  # noqa: F401