from django.urls import path, reverse_lazy
# This imports Django's path function, which is used to create URL routes for this app.
# reverse_lazy is used for redirect URLs in class-based authentication views.

from django.contrib.auth import views as auth_views
# This imports Django's built-in authentication views.
# These include the password reset views used to send reset emails and allow users to set a new password.

from . import views
# This imports the custom views.py file from the accounts app.
# The register and profile views are still custom views from this app.

app_name = "accounts"
# This gives the accounts app its own namespace.
# The register and profile pages can be linked as accounts:register and accounts:profile.

urlpatterns = [
    path("register/", views.register, name="register"),
    # This route opens the registration page.

    path("profile/", views.profile, name="profile"),
    # This route opens the logged-in user's profile page.

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
    # This route displays the password reset form and sends the reset email using the email backend configured in settings.py.

    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    # This route displays the confirmation page after the reset email has been sent.

    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
            success_url=reverse_lazy("accounts:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    # This route opens the secure reset link where the user can choose a new password.

    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    # This route displays the final confirmation after the password has been changed.
]