from django.urls import path, reverse_lazy
# This imports Django's path function for URL routes and reverse_lazy for redirect URLs used by class-based authentication views.

from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView
# These are Django's built-in views for setting a new password and showing the reset complete page.

from . import views
# This imports the custom views from accounts/views.py, including register, profile, and the demo password reset views.

app_name = "accounts"
# This gives the accounts app a namespace, so URLs can be called as accounts:register, accounts:profile, accounts:password_reset, etc.

urlpatterns = [
    # This list contains all URL routes that belong to the accounts app.

    path("register/", views.register, name="register"),
    # This route opens the user registration page at /accounts/register/.

    path("profile/", views.profile, name="profile"),
    # This route opens the logged-in user's profile page at /accounts/profile/.

    path("password_reset/", views.demo_password_reset, name="password_reset"),
    # This route opens the password reset form.
    # It uses the custom demo_password_reset view instead of Gmail SMTP, so the Render version works reliably.

    path("password_reset/done/", views.demo_password_reset_done, name="password_reset_done"),
    # This route opens the password reset result page.
    # For the academic Render demo, this page displays the secure reset link directly.

    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
            success_url=reverse_lazy("accounts:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    # This route lets the user set a new password after opening the secure reset link.

    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    # This route shows the final confirmation page after the password has been changed.
]