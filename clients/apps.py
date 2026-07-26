from django.apps import AppConfig
# This imports Django's AppConfig class, which is used to define configuration settings for a specific Django app.


class ClientsConfig(AppConfig):
    # This creates the configuration class for the clients app.
    # Django uses this class to recognise the app and apply any app-specific settings.
    # In the wider project, this connects the clients folder to the main Django project through INSTALLED_APPS in settings.py.
    default_auto_field = "django.db.models.BigAutoField"
    # This tells Django what type of automatic primary key field to use when a model does not define one manually.
    # BigAutoField creates a large auto-incrementing integer ID for each database record.
    # For example, every ClientProfile record in the clients app will automatically get an ID such as 1, 2, 3 and so on.
    # This is important because Django models need primary keys to uniquely identify rows in the PostgreSQL database.
    name = "clients"
    # This tells Django the exact name of the app folder.
    # The value "clients" must match the actual clients folder in the project.
    # This is how Django connects this app configuration to the clients app.
    # In the wider project, this app stores client profiles, financial profiles and risk assessments for the suitability review workflow.