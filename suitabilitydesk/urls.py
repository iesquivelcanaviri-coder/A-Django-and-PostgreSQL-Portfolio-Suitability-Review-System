"""Top-level URL configuration for SuitabilityDesk."""
from django.contrib import admin
# This imports Django's built-in admin site.
# The admin site lets the superuser manage database records through a browser instead of editing the database manually.
from django.contrib.auth import views as auth_views
# This imports Django's built-in authentication views, such as login, logout and password reset views.
# In this file, it is currently imported but not directly used because the project uses include("django.contrib.auth.urls") below instead.
from django.urls import include, path
# This imports the two main URL helper functions used in Django.
# path() creates a route, while include() connects another app's urls.py file to the main project urls.py file.
from dashboard import views as dashboard_views
# This imports the views.py file from the dashboard app and gives it the shorter name dashboard_views.
# This is useful because the public home page is connected directly from the main project URL file.

urlpatterns = [
# urlpatterns is the list Django reads when deciding what page to show for a requested URL.
# Each path inside this list connects a browser URL to either a view function or another urls.py file.
    path("admin/", admin.site.urls),
    # This creates the /admin/ route for the Django admin panel.
    # When I visit http://127.0.0.1:8000/admin/, Django sends me to the built-in admin interface.
    path("", dashboard_views.public_home, name="public_home"),
    # This creates the homepage route for the empty URL path.
    # The empty string "" means the root website address, for example http://127.0.0.1:8000/.
    # It connects the homepage to the public_home view inside dashboard/views.py.
    # The name="public_home" lets templates and redirects refer to this URL by name instead of hardcoding the path.
    path("dashboard/", include("dashboard.urls")),
    # This sends all URLs starting with /dashboard/ to the dashboard app's own urls.py file.
    # This keeps the main urls.py cleaner because dashboard-specific pages are managed inside the dashboard app.
    path("accounts/", include("accounts.urls")),
    # This sends all custom account-related URLs to the accounts app.
    # For example, registration and profile update pages can be handled inside accounts/urls.py.
    path("accounts/", include("django.contrib.auth.urls")),
    # This adds Django's built-in authentication URLs under the /accounts/ path.
    # It provides routes such as login, logout, password_change and password_reset if the matching templates exist.
    # This is important for the assignment because it supports authentication and password recovery.
    path("clients/", include("clients.urls")),
    # This sends all URLs starting with /clients/ to the clients app.
    # The clients app handles client profiles, financial profiles and risk assessments.
    path("mandates/", include("mandates.urls")),
    # This sends all URLs starting with /mandates/ to the mandates app.
    # The mandates app handles investment mandates, holdings, review projects, stakeholders and audit logs.
    path("messages/", include("messaging.urls")),
    # This sends all URLs starting with /messages/ to the messaging app.
    # The messaging app handles inbox, sent messages, read messages and archived messages.
]

# Overall, this file connects the whole Django project together by linking the main website routes to each individual app.