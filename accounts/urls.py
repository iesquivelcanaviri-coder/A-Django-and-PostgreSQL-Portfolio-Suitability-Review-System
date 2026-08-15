from django.urls import path, reverse_lazy
# This imports Django's path function for URL patterns and reverse_lazy for redirect URLs used by class-based views.

from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView
# These are Django's built-in views for setting a new password after the reset link is generated.

from . import views
# This imports the custom views from accounts/views.py, including register, profile and the demo password reset views.

app_name = "accounts"
# This gives the accounts app a namespace, so routes can be referenced as accounts:register, accounts:profile, etc.

urlpatterns = [
    path("register/", views.register, name="register"),
    # This route opens the user registration page at /accounts/register/.

    path("profile/", views.profile, name="profile"),
    # This route opens the logged-in user's profile page at /accounts/profile/.

    path("password_reset/", views.demo_password_reset, name="password_reset"),
    # This route opens the password reset request page.
    # It uses a custom academic/demo view so Render does not depend on Gmail or Brevo SMTP.

    path("password_reset/done/", views.demo_password_reset_done, name="password_reset_done"),
    # This route opens the password reset confirmation page.
    # For the Render demo, it displays the generated secure reset link directly on the page.

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
            template_name="registration/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
    # This route shows the final success page after the password has been changed.
]