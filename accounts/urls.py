from django.urls import path, reverse_lazy
# This imports Django's path function for URL routes and reverse_lazy for redirect URLs used by class-based auth views.

from django.contrib.auth import views as auth_views
# This imports Django's built-in authentication views, including password reset views.

from . import views
# This imports the custom views from accounts/views.py, such as register and profile.

app_name = "accounts"
# This sets the namespace for the accounts app URLs.
# Template links can use names such as accounts:register and accounts:profile.

urlpatterns = [
    path("register/", views.register, name="register"),
    # This route displays and processes the user registration page.

    path("profile/", views.profile, name="profile"),
    # This route displays and processes the logged-in user's profile page.

    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset_form.html",
            email_template_name="registration/password_reset_email.html",
            subject_template_name="registration/password_reset_subject.txt",
            success_url=reverse_lazy("accounts:password_reset_done"),
        ),
        name="password_reset",
    ),
    # This route shows the password reset form and sends the reset email if the submitted email belongs to an active user.

    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    # This route shows the confirmation page after the password reset request is submitted.

    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
            success_url=reverse_lazy("accounts:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    # This route lets the user set a new password using the secure reset token from the email.

    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    # This route shows the final confirmation page after the password has been changed.
]