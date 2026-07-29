from django.apps import AppConfig
# This imports Django's AppConfig class, which is used to define settings for one specific Django app.

class MessagingConfig(AppConfig):
    # This creates the configuration class for the messaging app, so Django knows how this app should be set up.
    default_auto_field = "django.db.models.BigAutoField"
    # This tells Django to use BigAutoField as the default primary key type for database tables in this app.
    # A primary key is the unique ID Django gives to each database record, for example each message in the Message table.
    # BigAutoField is useful because it supports a large number of records, which is good practice for database-backed apps.
    name = "messaging"
    # This tells Django the app's official name is "messaging".
    # Django uses this name to find the app's models, views, templates, URLs and migrations.
    # In the wider project, this connects the messaging folder to the internal inbox feature, where users can send, read and archive messages.