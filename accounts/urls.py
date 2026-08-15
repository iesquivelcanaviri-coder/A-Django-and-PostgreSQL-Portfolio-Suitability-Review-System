from django.urls import path, reverse_lazy
# This imports Django's path function for URL patterns and reverse_lazy for redirect URLs used by password reset views.

from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView
# This imports Django's built-in views for setting a new password and showing the password reset complete page.

from . import views
# This imports the views.py file from the current accounts app.

app_name = "accounts"
# This gives the accounts app its own namespace for custom account URLs such as accounts:register and accounts:profile.

urlpatterns = [
    path("register/", views.register, name="register"),
    # This route displays the registration page and saves new user accounts.

    path("profile/", views.profile, name="profile"),
    # This route displays and updates the logged-in user's profile.

    path("password_reset/", views.demo_password_reset, name="password_reset"),
    # This route displays the password reset form.
    # It creates a secure reset link without relying on Gmail SMTP, which makes the Render deployment more reliable.

    path("password_reset/done/", views.demo_password_reset_done, name="password_reset_done"),
    # This route displays the password reset link for the academic Render demonstration.

    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
            success_url=reverse_lazy("accounts:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    # This route lets the user open the secure reset link and choose a new password.

    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    # This route confirms that the password has been changed successfully.
]