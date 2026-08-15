from django.contrib.auth.views import PasswordResetCompleteView, PasswordResetConfirmView
# This imports Django's built-in views for the final two steps of the password reset workflow.
# PasswordResetConfirmView lets the user enter a new password after clicking the reset link.
# PasswordResetCompleteView shows the final success page after the password has been changed.

from django.urls import path, reverse_lazy
# path is used to create URL routes.
# reverse_lazy is used to safely refer to a named URL before Django has fully loaded all URL patterns.

from . import views
# This imports the views.py file from the current accounts app.
# The dot means "from this same app", so Django will look inside accounts/views.py.

app_name = "accounts"
# This gives all URLs in this file the accounts namespace.
# For example, templates can use {% url 'accounts:profile' %} or {% url 'accounts:password_reset' %}.


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
    # This uses the custom academic demo view instead of Gmail SMTP.

    path("password_reset/done/", views.demo_password_reset_done, name="password_reset_done"),
    # This route shows the generated reset link after the user submits their email.
    # Full URL: /accounts/password_reset/done/

    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
            success_url=reverse_lazy("accounts:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    # This route lets the user set a new password after opening the generated reset link.
    # The uidb64 part identifies the user securely.
    # The token part verifies that the reset request is valid.
    # Full URL example: /accounts/reset/MQ/token-value/

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