from django.contrib.auth.views import PasswordResetCompleteView, PasswordResetConfirmView
# This imports Django's built-in password reset views for the final stages of the reset workflow.
# PasswordResetConfirmView lets the user enter a new password after opening the generated reset link.
# PasswordResetCompleteView shows the success page after the password has been changed.

from django.urls import path, reverse_lazy
# path is used to define URL routes.
# reverse_lazy is used to safely point to another named URL before Django has finished loading all URL patterns.

from . import views
# This imports the views.py file from the current accounts app.
# The dot means "from this same app", so Django looks inside accounts/views.py.


app_name = "accounts"
# This gives the accounts app its own URL namespace.
# For example, templates can use {% url 'accounts:register' %}, {% url 'accounts:profile' %}, or {% url 'accounts:password_reset' %}.


urlpatterns = [
    # This list stores all URL routes for the accounts app.

    path("register/", views.register, name="register"),
    # This route shows the user registration page.
    # Full URL: /accounts/register/
    # Template link: {% url 'accounts:register' %}

    path("profile/", views.profile, name="profile"),
    # This route shows the logged-in user's profile page.
    # Full URL: /accounts/profile/
    # Template link: {% url 'accounts:profile' %}

    path("password_reset/", views.demo_password_reset, name="password_reset"),
    # This route shows the password reset request form.
    # Full URL: /accounts/password_reset/
    # This uses the custom academic demo view instead of relying on Gmail SMTP.
    # This is safer for Render because Gmail SMTP was causing the Gunicorn worker to crash.

    path("password_reset/done/", views.demo_password_reset_done, name="password_reset_done"),
    # This route shows the password reset result page.
    # Full URL: /accounts/password_reset/done/
    # In the academic Render demo, this page can display the secure reset link directly.

    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
            success_url=reverse_lazy("accounts:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    # This route lets the user set a new password after opening the generated reset link.
    # The uidb64 value identifies the user securely.
    # The token value checks that the reset request is valid.
    # Full URL example: /accounts/reset/MQ/example-token/

    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    # This route shows the final success page after the password has been changed.
    # Full URL: /accounts/reset/done/
]