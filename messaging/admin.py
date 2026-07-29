from django.contrib import admin
# This imports Django's built-in admin framework, which is the part of Django that gives us the ready-made admin dashboard for managing database records.
from .models import Message
# This imports the Message model from the current app's models.py file, so Django admin knows which database table we want to manage here.

@admin.register(Message)
# This registers the Message model with the Django admin site, meaning Message records will appear inside the /admin/ dashboard.
# The @admin.register() decorator is a cleaner way of writing admin.site.register(Message, MessageAdmin).
class MessageAdmin(admin.ModelAdmin):
    # This creates a custom admin class for the Message model.
    # It inherits from admin.ModelAdmin, which lets us control how Message records are displayed, searched and filtered in the Django admin panel.
    list_display = ("subject", "sender", "recipient", "sent_at", "is_read")
    # This controls which columns are shown in the admin list view for messages.
    # Instead of only seeing "Message object", I will see useful fields like the subject, sender, recipient, date sent and whether the message has been read.
    # This connects to the wider framework because Django admin reads these fields directly from the Message model and displays them as a database-backed table.
    list_filter = ("is_read", "sender_archived", "recipient_archived")
    # This adds filter options on the right side of the Django admin page.
    # It helps me quickly filter messages by read status and by whether the sender or recipient has archived the message.
    # This is useful because the messaging system has inbox/sent/archive behaviour, so the admin panel can inspect those states clearly.
    search_fields = ("subject", "body", "sender__username", "recipient__username")
    # This adds a search box to the admin page for Message records.
    # I can search by message subject, message body, sender username or recipient username.
    # The double underscore in sender__username and recipient__username means Django follows the relationship from Message to the related User model and searches the username field there.
    # This is an important ORM concept because it shows how Django can search across related database tables without writing raw SQL.