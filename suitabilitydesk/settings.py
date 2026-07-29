"""Project settings for SuitabilityDesk.
This file is intentionally deployment-ready: local development uses SQLite when no
DATABASE_URL is present, while Render/Neon can provide PostgreSQL through the same DATABASE_URL environment variable."""

from pathlib import Path
# Path is used to build file and folder paths in a safe way that works across different operating systems.
import os
# The os module lets this file read environment variables such as SECRET_KEY, DEBUG and DATABASE_URL.
import dj_database_url
# dj_database_url converts a database connection string into the dictionary format Django expects for DATABASES.
from dotenv import load_dotenv
# load_dotenv reads the local .env file, so private settings can stay outside GitHub.

load_dotenv()
# This loads values from the .env file into the environment before Django tries to read them.

BASE_DIR = Path(__file__).resolve().parent.parent
# BASE_DIR points to the main project folder, which helps Django locate files such as templates, static files and db.sqlite3.

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-before-deployment")
# SECRET_KEY is used by Django for security features such as sessions, password reset tokens and signed cookies.
# The value is read from the environment, but a development fallback is provided so the project can still run locally.
# In production on Render, this should always be a strong secret stored in Render Environment Variables.
DEBUG = os.environ.get("DEBUG", "False").lower() in {"true", "1", "yes"}
# DEBUG controls whether Django shows detailed error pages.
# This reads DEBUG from the environment and converts text like "True" or "1" into a real Python True value.
# For local development, DEBUG can be True, but for Render deployment it should be False.
ALLOWED_HOSTS = [host.strip() for host in os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") if host.strip()]
# ALLOWED_HOSTS tells Django which domains are allowed to serve this project.
# Locally, localhost and 127.0.0.1 are allowed by default.
# On Render, this must include the Render domain, for example a-django-and-postgresql-portfolio.onrender.com.
# The list comprehension splits comma-separated values from the environment into a clean Python list.
CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",") if origin.strip()]
# CSRF_TRUSTED_ORIGINS tells Django which full HTTPS origins are trusted for form submissions.
# This matters on Render because forms such as login, registration and profile update use CSRF protection.
# Unlike ALLOWED_HOSTS, this value should include https:// when used in production.

INSTALLED_APPS = [
    # INSTALLED_APPS tells Django which built-in and custom apps are active in this project.
    "django.contrib.admin",
    # Enables the Django admin panel, which is useful for managing users, clients, mandates and messages.
    "django.contrib.auth",
    # Enables Django's built-in authentication system for users, passwords, login and permissions.
    "django.contrib.contenttypes",
    # Supports Django's internal model tracking system and is required by auth and admin.
    "django.contrib.sessions",
    # Enables session handling, so Django can remember logged-in users between requests.
    "django.contrib.messages",
    # Enables temporary success/error messages, such as “Profile updated successfully”.
    "django.contrib.staticfiles",
    # Allows Django to manage CSS, JavaScript and image files.
    "accounts",
    # Custom app for user profiles, roles and profile-update functionality.
    "clients",
    # Custom app for client information, financial profiles and risk assessments.
    "mandates",
    # Custom app for investment mandates, holdings, projects, stakeholders and audit logs.
    "messaging",
    # Custom app for inbox, sent messages, read messages and archived messages.
    "dashboard",
    # Custom app for the homepage and dashboard summary pages.
]

MIDDLEWARE = [
    # MIDDLEWARE is a list of processing layers that run before and after each request.
    "django.middleware.security.SecurityMiddleware",
    # Adds security-related protections to requests and responses.
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # Allows the deployed Django app on Render to serve static files such as CSS and JavaScript.
    "django.contrib.sessions.middleware.SessionMiddleware",
    # Enables session support, which is needed for login and user state.
    "django.middleware.common.CommonMiddleware",
    # Provides common Django request/response behaviour, such as URL handling.
    "django.middleware.csrf.CsrfViewMiddleware",
    # Protects forms against Cross-Site Request Forgery attacks.
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    # Connects the logged-in user to each request as request.user.
    "django.contrib.messages.middleware.MessageMiddleware",
    # Enables Django messages to appear after redirects, such as success alerts.
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Helps protect the website from being embedded in another site in a harmful way.
]

ROOT_URLCONF = "suitabilitydesk.urls"
# ROOT_URLCONF tells Django which main urls.py file controls the project routes.

TEMPLATES = [
    # TEMPLATES tells Django how to find and render HTML template files.
    {
        # This dictionary configures the Django template engine.
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # This tells Django to use its normal built-in Django template system.
        "DIRS": [BASE_DIR / "templates"],
        # This tells Django to look in the main templates folder for shared templates such as base.html.
        "APP_DIRS": True,
        # This allows Django to also find templates inside each app's templates folder.
        "OPTIONS": {
            # OPTIONS contains extra template settings.
            "context_processors": [
                # Context processors automatically add useful variables to templates.
                "django.template.context_processors.debug",
                # Makes debugging-related information available to templates when DEBUG is enabled.
                "django.template.context_processors.request",
                # Makes the request object available in templates, which helps with navigation and user-specific logic.
                "django.contrib.auth.context_processors.auth",
                # Makes the logged-in user available in templates as user.
                "django.contrib.messages.context_processors.messages",
                # Makes Django flash messages available in templates.
            ],
        },
    },
]

WSGI_APPLICATION = "suitabilitydesk.wsgi.application"
# WSGI_APPLICATION points to the WSGI file used by Gunicorn when Render starts the live web app.

DATABASES = {
    # DATABASES defines the database connection used by Django's ORM.
    "default": dj_database_url.config(
        # The default database is configured using dj_database_url so Django can read DATABASE_URL from .env or Render.
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        # If DATABASE_URL is not available, Django falls back to local SQLite.
        # This makes local testing easier because the project can still run without PostgreSQL.
        conn_max_age=600,
        # Keeps database connections open for 600 seconds, which can improve performance.
        ssl_require=os.environ.get("DATABASE_SSL", "False").lower() in {"true", "1", "yes"},
        # Controls whether SSL is required for the database connection.
        # Neon usually uses SSL through the connection string, but this gives extra environment-based control.
    )
}

AUTH_PASSWORD_VALIDATORS = [
    # These validators help prevent weak passwords during user registration and admin user creation.
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    # Prevents passwords that are too similar to the user's personal information.
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    # Requires passwords to meet Django's minimum length rule.
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    # Blocks very common passwords such as “password123”.
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    # Blocks passwords that are entirely numeric.
]

LANGUAGE_CODE = "en-us"
# Sets the default language for Django text, dates and formatting.
TIME_ZONE = "Europe/Dublin"
# Sets the project time zone.
# This is suitable for an Ireland-based academic project and keeps timestamps consistent.
USE_I18N = True
# Enables Django internationalisation support, which means the project can support translations if needed later.
USE_TZ = True
# Stores datetimes in timezone-aware format, which is important for records such as messages and audit logs.

STATIC_URL = "static/"
# STATIC_URL is the URL prefix used when templates load CSS, JavaScript and image files.
STATICFILES_DIRS = [BASE_DIR / "static"]
# STATICFILES_DIRS tells Django where the source static files are during development.
STATIC_ROOT = BASE_DIR / "staticfiles"
# STATIC_ROOT is where collectstatic gathers all static files for production deployment.
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
# This tells Django and WhiteNoise to serve compressed static files with versioned filenames.
# It helps Render serve CSS and JavaScript properly in production.

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
# This sets the default primary key type for new models.
# BigAutoField gives each database record a large auto-incrementing ID.
LOGIN_REDIRECT_URL = "dashboard:home"
# After a successful login, Django redirects the user to the dashboard home page.
LOGOUT_REDIRECT_URL = "login"
# After logout, Django redirects the user back to the login page.

EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
# EMAIL_BACKEND controls how Django sends emails.
# The console backend prints emails to the terminal/logs, which is useful for testing password reset without a real email account.
EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
# EMAIL_HOST is the SMTP server used if real email sending is configured later.
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
# EMAIL_PORT is the mail server port.
# Port 587 is commonly used for TLS email sending.
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True").lower() in {"true", "1", "yes"}
# EMAIL_USE_TLS controls whether email sending uses TLS encryption.
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
# EMAIL_HOST_USER stores the email username if real SMTP email is used later.
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
# EMAIL_HOST_PASSWORD stores the email password or app password if real SMTP email is used.
# This must never be hardcoded or pushed to GitHub.
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "noreply@suitabilitydesk.local")
# DEFAULT_FROM_EMAIL is the sender address Django uses for password reset emails and system messages.

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# This tells Django to trust Render's proxy header when the original request was HTTPS.
# It is important for deployed apps because Render sits in front of Django and forwards secure requests.