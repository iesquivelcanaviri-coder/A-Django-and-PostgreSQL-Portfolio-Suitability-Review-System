from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "sender", "recipient", "sent_at", "is_read")
    list_filter = ("is_read", "sender_archived", "recipient_archived")
    search_fields = ("subject", "body", "sender__username", "recipient__username")
