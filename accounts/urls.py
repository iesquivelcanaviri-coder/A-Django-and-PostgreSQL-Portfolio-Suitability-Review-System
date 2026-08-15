from django.contrib.auth.views import PasswordResetCompleteView, PasswordResetConfirmView
# These are Django's built-in views for setting a new password after a valid reset link is opened.

from django.urls import path, reverse_lazy
# path creates URL patterns, and reverse_lazy is used for redirect URLs in class-based views.

from . import views
# This imports the custom view functions from accounts/views.py.


app_name = "accounts"
# This gives the accounts app its own namespace, such as accounts:register and accounts:profile.


urlpatterns = [
    # This list stores all URL routes that belong to the accounts app.

    path("register/", views.register, name="register"),
    # This route opens the registration page at /accounts/register/.
    # It requires a register function inside accounts/views.py.

    path("profile/", views.profile, name="profile"),
    # This route opens the logged-in user's profile page at /accounts/profile/.
    # It requires a profile function inside accounts/views.py.

    path("password_reset/", views.demo_password_reset, name="password_reset"),
    # This route opens the password reset request page.
    # It uses the custom demo_password_reset view so the Render version does not depend on Gmail SMTP.

    path("password_reset/done/", views.demo_password_reset_done, name="password_reset_done"),
    # This route opens the password reset result page.
    # For the academic Render demo, this page displays the generated secure reset link directly.

    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
            success_url=reverse_lazy("accounts:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    # This route opens the form where the user enters a new password after clicking the reset link.

    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    # This route shows the final confirmation page after the password has been changed.
]