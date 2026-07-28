from django.apps import AppConfig
# This imports AppConfig from Django, which is the base class Django uses to configure each app in the project.

class DashboardConfig(AppConfig):
    # This creates the configuration class for the dashboard app.
    # Django uses this class to recognise the app and connect it properly to the wider project.
    default_auto_field = "django.db.models.BigAutoField"
    # This tells Django what type of automatic primary key field to use when a model does not define its own primary key.
    # BigAutoField creates a large auto-incrementing integer ID, which is useful because it can support many database records.
    # In database terms, this is connected to the automatic ID column Django adds to tables.
    name = "dashboard"
    # This tells Django the actual Python app name.
    # The value must match the folder name of the app, which in this case is dashboard.
    # Django uses this name when the app is added to INSTALLED_APPS in settings.py.