"""Top-level URL configuration for SuitabilityDesk."""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from dashboard import views as dashboard_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", dashboard_views.public_home, name="public_home"),
    path("dashboard/", include("dashboard.urls")),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("clients/", include("clients.urls")),
    path("mandates/", include("mandates.urls")),
    path("messages/", include("messaging.urls")),
]
