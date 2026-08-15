from django.urls import path
# This imports Django's path function, which is used to connect a URL route to a view function.

from . import views
# This imports the views.py file from the current accounts app.
# The dot means "from this same app folder", so Django can find the register and profile views.

app_name = "accounts"
# This gives the accounts app its own namespace.
# For example, templates can link to the register page using {% url 'accounts:register' %}.

urlpatterns = [
    # This list stores the custom URL routes for the accounts app.

    path("register/", views.register, name="register"),
    # This route opens the registration page.
    # Full URL: /accounts/register/
    # It uses the custom register view from accounts/views.py.

    path("profile/", views.profile, name="profile"),
    # This route opens the logged-in user's profile page.
    # Full URL: /accounts/profile/
    # It uses the custom profile view from accounts/views.py.
]
# Password reset, login, logout and password change are handled by Django's built-in auth URLs.
# Those are included in the main suitabilitydesk/urls.py file using include("django.contrib.auth.urls").