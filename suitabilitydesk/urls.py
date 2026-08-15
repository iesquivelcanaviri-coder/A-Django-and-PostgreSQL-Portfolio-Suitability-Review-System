"""Top-level URL configuration for SuitabilityDesk."""
from django.contrib import admin
# This imports Django's built-in admin site.
from django.urls import include, path
# This imports include and path so the project can connect each app's URLs to the main project URL file.
from dashboard import views as dashboard_views
# This imports the dashboard views so the public home page can be connected directly here.


urlpatterns = [
    path("admin/", admin.site.urls),
    # This creates the /admin/ route for the Django admin panel.

    path("", dashboard_views.public_home, name="public_home"),
    # This creates the public homepage route.

    path("dashboard/", include("dashboard.urls")),
    # This sends all /dashboard/ URLs to the dashboard app.

    path("accounts/", include("accounts.urls")),
    # This sends custom account URLs such as registration, profile and custom password reset to accounts/urls.py.

    path("accounts/", include("django.contrib.auth.urls")),
    # This adds Django's built-in login, logout and password-change URLs.
    # The custom password reset routes in accounts.urls are listed first, so they take priority.

    path("clients/", include("clients.urls")),
    # This sends all /clients/ URLs to the clients app.

    path("mandates/", include("mandates.urls")),
    # This sends all /mandates/ URLs to the mandates app.

    path("messages/", include("messaging.urls")),
    # This sends all /messages/ URLs to the messaging app.

    path("updates/", include("updates.urls")),
    # This sends all /updates/ URLs to the updates app.
]