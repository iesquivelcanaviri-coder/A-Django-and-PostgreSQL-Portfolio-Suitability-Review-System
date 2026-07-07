"""Forms for registration and profile editing."""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


class RegisterForm(UserCreationForm):
    """Registration form using Django's secure built-in password handling."""
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]


class UserUpdateForm(forms.ModelForm):
    """Allows the logged-in user to update basic account details."""
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class UserProfileUpdateForm(forms.ModelForm):
    """Allows users to update contact details without changing their own role."""
    class Meta:
        model = UserProfile
        fields = ["phone", "organisation", "job_title"]
