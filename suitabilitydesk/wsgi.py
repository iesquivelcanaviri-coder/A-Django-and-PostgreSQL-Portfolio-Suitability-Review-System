"""WSGI config for SuitabilityDesk."""
import os
# This imports Python's built-in os module, which allows Django to work with environment variables and operating system settings.
from django.core.wsgi import get_wsgi_application
# This imports Django's get_wsgi_application function, which creates the WSGI application object needed by a production server.

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "suitabilitydesk.settings")
# This tells Django which settings file to use when the application starts.
# In this project, Django should load the settings from suitabilitydesk/settings.py.
# The setdefault method only sets this value if it has not already been set somewhere else, such as in Render environment variables.
application = get_wsgi_application()
# This creates the WSGI application object.
# A production server such as Gunicorn uses this application variable to run the Django project on Render.
# This connects the web server, Django settings, URL routing, views, templates, models and database-backed app logic together.