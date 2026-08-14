from django.urls import path, reverse_lazy
# This imports Django's path function, which is used to create URL patterns for this app.
# reverse_lazy is used for redirect URLs in class-based views, such as after a password reset is completed.

from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView
# This imports Django's built-in password reset confirmation and completion views.
# These views handle the page where the user enters a new password after opening the reset link.

from . import views
# This imports the views.py file from the current accounts app.
# The dot means "from this same folder/app", so Django will look for the register, profile and password reset views inside accounts/views.py.


app_name = "accounts"
# This sets a namespace for all URLs inside the accounts app.
# Namespacing is useful because bigger Django projects usually have many apps, and different apps might use similar URL names.
# For example, instead of just calling "profile", the project can clearly call "accounts:profile".
# This helps avoid confusion between profile pages or register pages in different parts of the project.


urlpatterns = [
    # urlpatterns is the list where this app stores its URL routes.
    # Django reads this list from top to bottom and checks whether the user's requested URL matches one of these paths.

    path("register/", views.register, name="register"),
    # This creates the URL route for the user registration page.
    # The full URL becomes /accounts/register/ because the main project urls.py includes this app under /accounts/.
    # The name="register" lets templates link to this page using {% url 'accounts:register' %}.

    path("profile/", views.profile, name="profile"),
    # This creates the URL route for the user profile page.
    # The full URL becomes /accounts/profile/.
    # This route is normally used after login because profile pages show or update private user information.

    path("password_reset/", views.demo_password_reset, name="password_reset"),
    # This creates the password reset request page.
    # It uses the custom demo_password_reset view instead of Gmail SMTP, so the deployed Render version can generate a reset link reliably.
    # The full URL becomes /accounts/password_reset/.

    path("password_reset/done/", views.demo_password_reset_done, name="password_reset_done"),
    # This creates the password reset done page.
    # For the academic Render deployment, this page can display the generated secure reset link instead of relying on Gmail delivery.
    # The full URL becomes /accounts/password_reset/done/.

    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
            success_url=reverse_lazy("accounts:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    # This creates the secure password reset confirmation URL.
    # uidb64 identifies the user safely, and token is Django's secure reset token.
    # This page lets the user enter and confirm a new password.
    # The full URL looks like /accounts/reset/<uidb64>/<token>/.

    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
    # This creates the final password reset completion page.
    # It appears after the user successfully changes their password.
    # The full URL becomes /accounts/reset/done/.
]
# These routes only become part of the full website because the main project urls.py includes this file using path("accounts/", include("accounts.urls")).