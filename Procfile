
# The Procfile tells the hosting platform how to start your web application.
# "web:" means this is the main web process that will handle HTTP requests.
# Platforms like Render or Heroku read this file to know what command to run.

# "gunicorn" is a production-ready web server for Python applications.
# It replaces Django's built-in development server, which is NOT safe for production.

# "suitabilitydesk.wsgi:application" points to your Django project's WSGI entry point.
# WSGI = Web Server Gateway Interface, the standard way Python web apps talk to web servers.
# This tells gunicorn: “Load the WSGI application object from suitabilitydesk/wsgi.py”.

web: gunicorn suitabilitydesk.wsgi:application
