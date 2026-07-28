from django.urls import path
# This imports Django's path function, which is used to connect a URL pattern to a view function.
from . import views
# This imports the views.py file from the same dashboard app folder.
# The dot means "look in the current app", so Django knows to use dashboard/views.py.

app_name = "dashboard"
# This gives the dashboard app its own namespace.
# A namespace helps Django identify URLs clearly when different apps may have similar URL names.
# For example, the dashboard app can have a URL called "home" without confusing it with another app's "home" URL.
urlpatterns = [
# This list stores all the URL routes that belong to the dashboard app.
# Django reads this list to know which view should run when a user visits a certain web address.
    path("", views.home, name="home"),
    # This route points to the dashboard home page.
    # The empty string "" means this is the default page for the dashboard app.
    # For example, if the main project urls.py includes dashboard.urls at the root path, this could load at http://127.0.0.1:8000/.
    # views.home tells Django to run the home function from dashboard/views.py.
    # name="home" gives this URL a reusable name, so templates and views can link to it using {% url 'dashboard:home' %}.
]
# Any new dashboard pages, such as reports or analytics, would be added inside this list.