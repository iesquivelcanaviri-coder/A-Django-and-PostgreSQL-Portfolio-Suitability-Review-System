"""Internal inbox and archive models."""

from django.conf import settings
# This imports Django settings so the model can refer to the active user model in a flexible way instead of hardcoding Django's default User model.
from django.db import models
# This imports Django's model tools, which are used to create database tables through Python classes.
from mandates.models import PortfolioReviewProject
# This imports the PortfolioReviewProject model so a message can optionally be linked to a specific portfolio review project.

class Message(models.Model):
    # This creates a Django model called Message, meaning Django will create a database table for storing internal user messages.
    """Stores internal messages between users with inbox, sent and archive states."""
    # This explains the purpose of the model: it stores messages sent from one user to another and tracks inbox/archive behaviour.
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        # This links the message to the user who sent it, using the active user model from Django settings.
        on_delete=models.CASCADE,
        # If the sender user is deleted, their sent messages will also be deleted, which keeps the database clean.
        related_name="sent_messages"
        # This lets Django access all messages sent by a user using user.sent_messages.all().
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        # This links the message to the user who receives it, again using Django's configured user model.
        on_delete=models.CASCADE,
        # If the recipient user is deleted, their received messages will also be deleted.
        related_name="received_messages"
        # This lets Django access all messages received by a user using user.received_messages.all().
    )
    subject = models.CharField(max_length=180)
    # This stores the message subject as short text, with a maximum length of 180 characters.
    body = models.TextField()
    # This stores the full message content, using TextField because the body can be longer than a normal CharField.
    related_project = models.ForeignKey(
        PortfolioReviewProject,
        # This optionally connects the message to a portfolio review project, which helps link communication to project evidence.
        on_delete=models.SET_NULL,
        # If the related project is deleted, the message is kept but the project link becomes empty instead of deleting the message.
        null=True,
        # This allows the database to store NULL when a message is not connected to a project.
        blank=True,
        # This allows the related project field to be optional in Django forms and admin screens.
        related_name="messages"
        # This lets Django access all messages linked to a project using project.messages.all().
    )
    sent_at = models.DateTimeField(auto_now_add=True)
    # This automatically stores the date and time when the message is first created.
    is_read = models.BooleanField(default=False)
    # This tracks whether the recipient has opened/read the message; new messages start as unread.
    sender_archived = models.BooleanField(default=False)
    # This tracks whether the sender has archived the message from their sent folder view.
    recipient_archived = models.BooleanField(default=False)
    # This tracks whether the recipient has archived the message from their inbox view.

    class Meta:
        # Meta is an inner Django class used to add extra model settings that affect database queries and admin behaviour.
        ordering = ["-sent_at"]
        # This orders messages by newest first whenever messages are queried without a custom order.

    def __str__(self):
        # This method controls how the message appears as text in the Django admin, shell, and dropdowns.
        return self.subject
        # This returns the message subject as the readable display name for each Message object.