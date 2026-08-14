from django.contrib.auth.views import PasswordResetCompleteView, PasswordResetConfirmView
# These are Django's built-in views for setting a new password after a reset link has been generated.

from django.urls import path, reverse_lazy
# path connects URLs to views, and reverse_lazy helps redirect after the password reset is complete.

from . import views
# This imports the custom views from accounts/views.py.

app_name = "accounts"
# This gives the accounts app a namespace, so URLs can be referred to as accounts:profile, accounts:register, etc.

urlpatterns = [
    path("register/", views.register, name="register"),
    # This route displays and processes the user registration form.

    path("profile/", views.profile, name="profile"),
    # This route displays and updates the logged-in user's profile.

    path("password_reset/", views.demo_password_reset, name="password_reset"),
    # This route displays the password reset form and creates a secure reset link for the academic Render demo.

    path("password_reset/done/", views.demo_password_reset_done, name="password_reset_done"),
    # This route displays the generated reset link after the user submits their email address.

    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
            success_url=reverse_lazy("accounts:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    # This route lets the user choose a new password after opening the secure reset link.

    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    # This route confirms that the password reset has been completed.
]