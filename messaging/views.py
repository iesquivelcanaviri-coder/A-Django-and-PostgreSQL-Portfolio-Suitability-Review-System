"""Inbox, sent, archive and compose views."""
from django.contrib import messages
# Imports Django's messages framework, which lets the app show success/error messages to the user after actions like sending or archiving a message.
from django.contrib.auth.decorators import login_required
# Imports the login_required decorator, which protects views so only logged-in users can access private messaging pages.
from django.core.exceptions import PermissionDenied
# Imports PermissionDenied so the view can block users if they try to access a message that does not belong to them.
from django.shortcuts import get_object_or_404, redirect, render
# Imports common Django shortcut functions: render loads templates, redirect sends the user to another page, and get_object_or_404 safely finds a database object or shows a 404 error.
from .forms import MessageForm
# Imports the MessageForm from this app's forms.py file, so the compose view can display and validate the message form.
from .models import Message
# Imports the Message model from models.py, which represents the database table storing inbox, sent and archived messages.

@login_required
# This decorator means the user must be logged in before they can view their inbox.
def inbox(request):
    # Defines the inbox view function, which receives the request object from Django when the user visits the inbox URL.
    msgs = Message.objects.filter(recipient=request.user, recipient_archived=False)
    # Gets messages from the database where the logged-in user is the recipient and has not archived them.
    return render(request, "messaging/inbox.html", {"messages_list": msgs, "box_title": "Inbox"})
    # Sends the inbox messages to the inbox.html template and sets the page title/context label as "Inbox".

@login_required
# This decorator protects the sent messages page so only logged-in users can access it.
def sent(request):
    # Defines the sent view function, which shows messages that the current user has sent.
    msgs = Message.objects.filter(sender=request.user, sender_archived=False)
    # Gets messages from the database where the logged-in user is the sender and has not archived them from their sent box.
    return render(request, "messaging/inbox.html", {"messages_list": msgs, "box_title": "Sent Messages"})
    # Reuses the same inbox.html template, but changes the data and title so it displays sent messages instead of received messages.

@login_required
# This decorator protects the archived messages page from users who are not logged in.
def archived(request):
    # Defines the archived view function, which shows messages archived by the current user.
    msgs = Message.objects.filter(recipient=request.user, recipient_archived=True) | Message.objects.filter(sender=request.user, sender_archived=True)
    # Gets messages where the user archived them as a recipient OR archived them as a sender; the | symbol combines both querysets.
    return render(request, "messaging/inbox.html", {"messages_list": msgs.distinct(), "box_title": "Archived Messages"})
    # Sends the archived messages to the inbox.html template and uses distinct() to avoid showing duplicates if a message appears in both querysets.

@login_required
# This decorator makes sure only logged-in users can compose and send messages.
def compose(request):
    # Defines the compose view function, which handles both showing the message form and processing submitted messages.
    if request.method == "POST":
        # Checks whether the form has been submitted, because POST requests usually mean the user sent data from a form.
        form = MessageForm(request.POST)
        # Creates a MessageForm using the submitted form data from the request.
        if form.is_valid():
            # Checks whether the submitted form data passes Django's validation rules from forms.py and the model fields.
            msg = form.save(commit=False)
            # Creates a message object from the form but does not save it yet, because the sender must be added first.
            msg.sender = request.user
            # Sets the sender of the message to the currently logged-in user, so users cannot fake who sent the message.
            msg.save()
            # Saves the completed message object to the database.
            messages.success(request, "Message sent.")
            # Adds a success message that can be displayed on the next page to confirm that the message was sent.
            return redirect("messaging:sent")
            # Redirects the user to the sent messages page after the message is saved, following the POST-redirect-GET pattern.
    else:
        # Runs when the user first opens the compose page using a normal GET request.
        form = MessageForm()
        # Creates a blank MessageForm so the user can fill in a new message.
    return render(request, "messaging/compose.html", {"form": form})
    # Renders the compose.html template and passes the form into the template context.


@login_required
# This decorator protects the message detail page so only logged-in users can view message contents.
def detail(request, pk):
    # Defines the detail view function, where pk is the primary key of the message being opened.
    msg = get_object_or_404(Message, pk=pk)
    # Looks for the message with the matching primary key; if it does not exist, Django shows a 404 page instead of crashing.
    if request.user not in {msg.sender, msg.recipient}:
        # Checks whether the logged-in user is either the sender or the recipient of the message.
        raise PermissionDenied("You can only read messages that you sent or received.")
        # Blocks access if the user is not connected to this message, which protects private inbox data.
    if request.user == msg.recipient and not msg.is_read:
        # Checks if the logged-in user is the recipient and the message has not already been marked as read.
        msg.is_read = True
        # Changes the message status to read, which helps the dashboard or inbox count unread messages correctly.
        msg.save(update_fields=["is_read"])
        # Saves only the is_read field to the database, which is more efficient than saving every field again.
    return render(request, "messaging/message_detail.html", {"message_obj": msg})
    # Renders the message detail page and passes the selected message into the template as message_obj.

@login_required
# This decorator makes sure only logged-in users can archive messages.
def archive_message(request, pk):
    # Defines the archive_message view function, where pk identifies which message should be archived.
    msg = get_object_or_404(Message, pk=pk)
    # Gets the message from the database or returns a 404 error if the message does not exist.
    if request.user == msg.recipient:
        # Checks whether the logged-in user is the recipient of the message.
        msg.recipient_archived = True
        # Archives the message only for the recipient, so the sender's copy is not automatically affected.
    elif request.user == msg.sender:
        # If the user is not the recipient, this checks whether the logged-in user is the sender.
        msg.sender_archived = True
        # Archives the message only for the sender, so the recipient can still see their own copy.
    else:
        # Runs if the logged-in user is neither the sender nor the recipient.
        raise PermissionDenied("You can only archive your own messages.")
        # Blocks the action because users should not archive messages that do not belong to them.
    msg.save()
    # Saves the archive status change to the database.
    messages.success(request, "Message archived.")
    # Adds a confirmation message so the user knows the archive action worked.
    return redirect("messaging:inbox")
    # Sends the user back to the inbox after archiving the message.