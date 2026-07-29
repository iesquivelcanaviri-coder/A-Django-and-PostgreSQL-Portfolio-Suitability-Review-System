"""ASGI config for SuitabilityDesk."""
import os
# This imports Python's built-in os module, which lets Django read and set environment variables.
# In this file, it is mainly used to tell Django which settings file belongs to the project.
from django.core.asgi import get_asgi_application
# This imports Django's get_asgi_application function.
# The function creates the ASGI application object that a web server can use to run the Django project.

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "suitabilitydesk.settings")
# This sets the default Django settings module for the project.
# "suitabilitydesk.settings" points Django to the settings.py file inside the suitabilitydesk folder.
# This is important because Django needs settings.py to know the installed apps, database connection, templates, static files and security settings.
application = get_asgi_application()
# This creates the ASGI application object.
# The variable must usually be called application because deployment servers look for this name when starting the project.
# In the wider framework picture, this line connects the Django project code to the server process that will serve the web app.