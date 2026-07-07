"""WSGI config for SuitabilityDesk."""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "suitabilitydesk.settings")
application = get_wsgi_application()
