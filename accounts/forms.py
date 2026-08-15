from django import forms
# This imports Django's forms system.

from django.contrib.auth.models import User
# This imports Django's built-in User model.

from django.contrib.auth.forms import UserCreationForm
# This imports Django's built-in registration form.

from .models import UserProfile
# This imports the custom UserProfile model from accounts/models.py.


class RegisterForm(UserCreationForm):
    # This form extends Django's built-in UserCreationForm so users can register with username, email and password.

    email = forms.EmailField(required=True)
    # This adds an email field to the registration form and makes it required.

    class Meta:
        # The Meta class tells Django which model and fields this form uses.

        model = User
        # This connects the form to Django's built-in User model.

        fields = ["username", "email", "password1", "password2"]
        # These are the fields shown on the registration page.


class UserProfileForm(forms.ModelForm):
    # This form lets users update their profile information.

    class Meta:
        # The Meta class tells Django which model and fields belong to this form.

        model = UserProfile
        # This connects the form to the UserProfile model.

        fields = ["role", "phone", "organisation", "job_title"]
        # These fields must exist in your UserProfile model.