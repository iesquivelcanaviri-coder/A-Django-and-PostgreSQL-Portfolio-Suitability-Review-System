from django.urls import path, reverse_lazy
# This imports Django's path function and reverse_lazy.
# path connects URL patterns to views.
# reverse_lazy is used for password reset success redirects because URL names are resolved later when Django starts.

from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView
# These are Django's built-in views for setting a new password after a reset link has been generated.
# PasswordResetConfirmView shows the new password form.
# PasswordResetCompleteView shows the final success page.

from . import views
# This imports the views.py file from the current accounts app.
# The dot means "from this same folder/app".

app_name = "accounts"
# This sets a namespace for normal account routes such as accounts:register and accounts:profile.

urlpatterns = [
    path("register/", views.register, name="register"),
    # This creates the registration page at /accounts/register/.

    path("profile/", views.profile, name="profile"),
    # This creates the profile page at /accounts/profile/.

    path("password_reset/", views.demo_password_reset, name="password_reset"),
    # This creates the password reset request page at /accounts/password_reset/.
    # This uses the custom demo_password_reset view from accounts/views.py.

    path("password_reset/done/", views.demo_password_reset_done, name="password_reset_done"),
    # This creates the password reset done page at /accounts/password_reset/done/.
    # This page can show the generated reset link for the academic Render demo.

    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
            success_url=reverse_lazy("password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    # This route opens the secure password reset confirmation page.
    # The uidb64 and token values come from Django's password reset token system.
    # The user enters a new password on this page.

    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
    # This route shows the final page after the password has been changed successfully.
]

