from django.urls import path, reverse_lazy
# This imports Django's path function, which is used to connect URLs to views.
# reverse_lazy is used for password reset redirect URLs because Django can resolve the URL name later when the view runs.

from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView
# These are Django's built-in class-based views for setting a new password after a reset link has been generated.
# PasswordResetConfirmView shows the form where the user enters the new password.
# PasswordResetCompleteView shows the success page after the password has been changed.

from . import views
# This imports the views.py file from the current accounts app.
# The dot means Django should look inside this same app folder.


app_name = "accounts"
# This gives the accounts app its own namespace.
# This means URLs can be linked clearly using names such as accounts:register, accounts:profile, or accounts:password_reset.


urlpatterns = [
    # This list stores all the URL routes for the accounts app.

    path("register/", views.register, name="register"),
    # This route opens the user registration page.
    # The full URL will usually be /accounts/register/.
    # It calls the register view from accounts/views.py.

    path("profile/", views.profile, name="profile"),
    # This route opens the logged-in user's profile page.
    # The full URL will usually be /accounts/profile/.
    # It calls the profile view from accounts/views.py.

    path("password_reset/", views.demo_password_reset, name="password_reset"),
    # This route opens the password reset request page.
    # It uses a custom view so the deployed Render demo does not depend on Gmail SMTP.
    # The full URL will usually be /accounts/password_reset/.

    path("password_reset/done/", views.demo_password_reset_done, name="password_reset_done"),
    # This route opens the password reset confirmation page after the email form is submitted.
    # For the academic Render deployment, this page can display the secure reset link directly.

    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
            success_url=reverse_lazy("accounts:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    # This route opens the secure page where the user enters a new password.
    # uidb64 identifies the user securely, while token verifies that the reset link is valid.
    # If the password change succeeds, Django redirects to accounts:password_reset_complete.

    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    # This route shows the final success page after the password has been changed.
]