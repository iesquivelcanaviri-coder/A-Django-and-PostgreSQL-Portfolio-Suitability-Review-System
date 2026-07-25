# This imports AppConfig, which is Django's base class for app configuration.
# Each Django app can have its own configuration class so Django knows how to load and manage that app.
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    # This tells Django what type of primary key field to create automatically
    # when a model does not define its own primary key.
    # BigAutoField creates a 64-bit integer ID field, which is useful because it
    # can handle a very large number of records. Django now commonly uses this
    # as the default for new projects.
    # Example: If I create a UserProfile model and do not manually add an id field,
    # Django will automatically create something like:
    # id = models.BigAutoField(primary_key=True)
    default_auto_field = "django.db.models.BigAutoField"

    # This is the name of this Django app.
    # It must match the folder name of the app, which in this case is:
    # accounts/
    # Django uses this value when the app is added to INSTALLED_APPS in settings.py.
    # For example:
    # INSTALLED_APPS = [
    #     "accounts",
    # ]
    # or sometimes:
    # INSTALLED_APPS = [
    #     "accounts.apps.AccountsConfig",
    # ]
    # This connects the accounts app to the whole Django project.
    name = "accounts"

    def ready(self):
        # The ready() method runs when Django has finished loading the app.
        # I am using it here to import accounts.signals so that my signal functions
        # become active when the project starts.
        # In this project, signals are useful because they can automatically create
        # or update a UserProfile when a Django User is created or saved.
        # Wider Django connection:
        # - The User model comes from Django's built-in authentication system.
        # - The UserProfile model extends the user with extra details such as role,
        #   phone number, organisation and job title.
        # - The signal links both models together automatically.
        # This means when a user registers, Django can automatically create the
        # matching profile without needing to manually create it in every view.
        # The noqa comment tells code checkers not to complain that the import is
        # unused. Even though it looks unused, it is needed because importing the
        # file registers the signal handlers with Django.
        import accounts.signals  # noqa: F401