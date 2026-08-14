from django.urls import path
# This imports Django's path function, which is used to connect a URL pattern to a view function.

from . import views
# This imports the views.py file from the current accounts app.
# The dot means Django should import views from this same accounts folder.

app_name = "accounts"
# This gives the accounts app its own namespace.
# For example, templates can use {% url 'accounts:register' %} and {% url 'accounts:profile' %}.


urlpatterns = [
    # This list stores the custom account URLs that belong to the accounts app.

    path("register/", views.register, name="register"),
    # This creates the registration URL.
    # Because the main project includes this app under /accounts/, the full URL becomes /accounts/register/.
    # It connects to the register view inside accounts/views.py.

    path("profile/", views.profile, name="profile"),
    # This creates the profile URL.
    # Because the main project includes this app under /accounts/, the full URL becomes /accounts/profile/.
    # It connects to the profile view inside accounts/views.py.
]
# Password reset URLs are not placed here because they need global URL names such as password_reset.
# Those routes are defined in suitabilitydesk/urls.py so the login template can use {% url 'password_reset' %}.