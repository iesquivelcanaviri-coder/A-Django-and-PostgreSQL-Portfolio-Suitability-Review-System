"""Internal inbox and archive models."""
from django.conf import settings
from django.db import models
from mandates.models import PortfolioReviewProject


class Message(models.Model):
    """Stores internal messages between users with inbox, sent and archive states."""
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_messages")
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="received_messages")
    subject = models.CharField(max_length=180)
    body = models.TextField()
    related_project = models.ForeignKey(PortfolioReviewProject, on_delete=models.SET_NULL, null=True, blank=True, related_name="messages")
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    sender_archived = models.BooleanField(default=False)
    recipient_archived = models.BooleanField(default=False)

    class Meta:
        ordering = ["-sent_at"]

    def __str__(self):
        return self.subject
