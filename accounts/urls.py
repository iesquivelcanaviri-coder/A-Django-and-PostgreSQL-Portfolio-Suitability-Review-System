from django.urls import path
# This imports Django's path function so this app can define its own URL routes.

from . import views
# This imports the views.py file from the accounts app.

app_name = "accounts"
# This gives the accounts app a namespace, so templates can use names such as accounts:register and accounts:profile.

urlpatterns = [
    path("register/", views.register, name="register"),
    # This route opens the registration page.

    path("profile/", views.profile, name="profile"),
    # This route opens the logged-in user's profile page.

    path("password_reset/", views.demo_password_reset, name="password_reset"),
    # This route replaces Django's normal password reset form with the academic demo version.
    # It creates a secure reset link without relying on Gmail SMTP.

    path("password_reset/done/", views.demo_password_reset_done, name="password_reset_done"),
    # This route shows the generated reset link after the user submits their email.
]