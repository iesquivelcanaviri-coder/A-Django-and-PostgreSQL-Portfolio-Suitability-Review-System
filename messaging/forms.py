from django import forms
# Imports Django's forms module, which gives us tools for creating HTML forms from Python code instead of writing every form field manually in the template.
from .models import Message
# Imports the Message model from the current app's models.py file, so this form can be directly connected to the database table for messages.

class MessageForm(forms.ModelForm):
    # Creates a Django ModelForm for the Message model.
    # A ModelForm is useful because it automatically builds form fields based on the model fields.
    # In this project, this helps connect the inbox/message form directly to the messaging database table.
    class Meta:
        # The Meta class gives Django instructions about which model this form is based on and which fields should appear in the form.
        # This is part of Django's form framework, where the form is linked to the database model in a clean and reusable way.
        model = Message
        # Tells Django that this form is based on the Message model.
        # This means when the form is saved, Django knows it should create or update a Message object in the database.
        fields = ["recipient", "subject", "body", "related_project"]
        # Lists the specific Message model fields that should appear in the form.
        # recipient allows the sender to choose who the message is going to.
        # subject stores the short title or topic of the message.
        # body stores the main message content.
        # related_project links the message to a portfolio review project, which helps connect communication to the wider suitability review workflow.