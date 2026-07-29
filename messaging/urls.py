from django.urls import path
# This imports Django's path function, which is used to connect a URL pattern to a view function
from . import views
# This imports the views.py file from the same messaging app folder, so each URL can call the correct view function.

app_name = "messaging"
# This gives the messaging app its own namespace, so links can be written clearly as messaging:inbox, messaging:compose, etc.
# This is useful in bigger Django projects because different apps might use the same URL names, such as "detail" or "create".

urlpatterns = [
# This list stores all the URL routes that belong to the messaging app.
# Django reads this list when it needs to match a browser URL to a specific view.
    path("", views.inbox, name="inbox"),
    # This route is for the main messaging page.
    # The empty string "" means this is the default page when the user visits the messaging app URL.
    # It calls the inbox view from views.py, which should display received messages.
    # The name "inbox" allows templates to link to this page using {% url 'messaging:inbox' %}.
    path("sent/", views.sent, name="sent"),
    # This route handles the sent messages page.
    # When the user visits /sent/ inside the messaging section, Django calls the sent view.
    # This should show messages that the logged-in user has sent to other users.
    # The name "sent" can be used in templates with {% url 'messaging:sent' %}.
    path("archived/", views.archived, name="archived"),
    # This route handles the archived messages page.
    # It calls the archived view, which should show messages the user has moved out of the active inbox.
    # This supports the assignment requirement for inbox/archive functionality.
    # The name "archived" makes it easier to create links without hardcoding the URL.
    path("compose/", views.compose, name="compose"),
    # This route handles the compose message page.
    # When the user visits /compose/, Django calls the compose view.
    # This view should normally show a form where the user can write and send a new internal message.
    # The name "compose" can be used in buttons or navbar links, for example {% url 'messaging:compose' %}.
    path("<int:pk>/", views.detail, name="detail"),
    # This route handles the detail page for one specific message.
    # <int:pk> means Django expects an integer in the URL, such as /5/.
    # The pk value usually represents the primary key ID of a Message record in the database.
    # Django passes this pk into the detail view, so the view can find and display the correct message.
    # The name "detail" allows templates to link to a specific message using {% url 'messaging:detail' message.pk %}.
    path("<int:pk>/archive/", views.archive_message, name="archive"),
    # This route handles archiving one specific message.
    # <int:pk> again captures the message ID from the URL.
    # Django sends that ID to the archive_message view, so the correct message can be marked as archived.
    # This is not deleting the message completely; it usually updates an archive field in the database.
    # The name "archive" allows templates to create archive buttons using {% url 'messaging:archive' message.pk %}.
]
