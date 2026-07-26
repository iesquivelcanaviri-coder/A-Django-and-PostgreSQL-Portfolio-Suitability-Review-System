from django.urls import path
# This imports Django's path function, which is used to create URL patterns for this app.
# In Django, a URL pattern connects a web address to a view, so Django knows what code to run when a user visits a page.
from . import views
# This imports the views.py file from the current accounts app.
# The dot means "from this same folder/app", so Django will look for the register and profile view functions inside accounts/views.py.

app_name = "accounts"
# This sets a namespace for all URLs inside the accounts app.
# Namespacing is useful because bigger Django projects usually have many apps, and different apps might use similar URL names.
# For example, instead of just calling "profile", the project can clearly call "accounts:profile".
# This helps avoid confusion between profile pages or register pages in different parts of the project.

urlpatterns = [
    # urlpatterns is the list where this app stores its URL routes.
    # Django reads this list from top to bottom and checks whether the user's requested URL matches one of these paths.
    # Each path connects a small URL pattern to a specific view function and gives it a name for easier linking in templates.
    path("register/", views.register, name="register"),
    # This creates the URL route for the user registration page.
    # The first part, "register/", is the URL ending that belongs to this accounts app.
    # The second part, views.register, tells Django to run the register function from accounts/views.py when this URL is visited.
    # The name="register" part gives this route a reusable name.
    # Because this file uses app_name = "accounts", templates can link to this page using {% url 'accounts:register' %}.
    # This is better than hardcoding the URL because if the URL path changes later, the template link can still work through the route name.
    path("profile/", views.profile, name="profile"),
    # This creates the URL route for the user profile page.
    # The first part, "profile/", is the URL ending for the profile page inside the accounts app.
    # The second part, views.profile, tells Django to run the profile function from accounts/views.py.
    # The name="profile" part gives this URL a shortcut name.
    # Because of the accounts namespace, this page can be linked in templates as {% url 'accounts:profile' %}.
    # This route is normally used after login, because profile pages usually show or update private user information.
]
# These routes only become part of the full website if the main project urls.py includes the accounts app URLs.
# For example, the main suitabilitydesk/urls.py might include this file using path("accounts/", include("accounts.urls")).
# If that is the case, the full registration URL becomes /accounts/register/ and the full profile URL becomes /accounts/profile/.