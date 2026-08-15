from django.urls import path, reverse_lazy
# This imports Django's path function for URL routes and reverse_lazy for redirect URLs used by password reset views.

from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView
# These are Django's built-in views for setting a new password and showing the final password reset complete page.

from . import views
# This imports the views.py file from the accounts app.

app_name = "accounts"
# This gives all accounts app URLs a namespace, so templates can use names such as accounts:register and accounts:profile.

urlpatterns = [
    path("register/", views.register, name="register"),
    # This route displays the registration page and creates new user accounts.

    path("profile/", views.profile, name="profile"),
    # This route displays the logged-in user's profile page.

    path("password_reset/", views.demo_password_reset, name="password_reset"),
    # This route displays the password reset form and creates a secure reset link without relying on Gmail SMTP.

    path("password_reset/done/", views.demo_password_reset_done, name="password_reset_done"),
    # This route displays the generated reset link for the Render academic demonstration.

    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
            success_url=reverse_lazy("accounts:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    # This route opens the secure page where the user enters a new password.

    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
    # This route shows the final success page after the password has been changed.
]