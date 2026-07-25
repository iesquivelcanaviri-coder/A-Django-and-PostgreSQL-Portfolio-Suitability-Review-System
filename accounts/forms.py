"""Forms for registration and profile editing."""
# This file contains the Django forms used by the accounts app.
# In Django, forms.py is normally where we define how users enter or update data.
# These forms connect the HTML templates to Django models and help validate user input before saving it to the database.

from django import forms
# This imports Django's forms module.
# I need this because ModelForm and fields such as EmailField and CharField come from Django's form system.
# Django forms are useful because they reduce the amount of manual HTML and validation code I need to write.

from django.contrib.auth.forms import UserCreationForm
# UserCreationForm is Django's built-in registration form.
# It already includes secure password validation and password confirmation.
# This is better than writing password logic manually because Django already handles password hashing safely.

from django.contrib.auth.models import User
# This imports Django's built-in User model.
# The User model stores the standard account information such as username, first name, last name, email and password.
# In this project, I use the built-in User model for login and authentication instead of creating my own user table from scratch.

from .models import UserProfile
# This imports the UserProfile model from the accounts app.
# UserProfile stores extra user information that is not included in Django's default User model.
# For this project, it stores details such as phone, organisation, job title and role.


class RegisterForm(UserCreationForm):
    """Registration form using Django's secure built-in password handling."""
    # This class creates the registration form for new users.
    # It inherits from UserCreationForm, so it already has username, password1 and password2 fields.
    # I extend it by adding email, first name and last name because these are useful for identifying users in the system.

    email = forms.EmailField(required=True)
    # This adds an email field to the registration form.
    # required=True means the user cannot submit the registration form without entering an email.
    # Django will also check that the value entered looks like a valid email address.

    first_name = forms.CharField(max_length=150, required=True)
    # This adds a first name field to the registration form.
    # max_length=150 matches Django's built-in User model limit for first_name.
    # required=True makes sure the user provides their first name during registration.

    last_name = forms.CharField(max_length=150, required=True)
    # This adds a last name field to the registration form.
    # This helps make the account more complete and professional for the portfolio suitability system.
    # It is useful because users in the system may be advisers, clients, portfolio managers or compliance reviewers.

    class Meta:
        # The Meta class tells Django which model this form is connected to and which fields should appear.
        # This is a common Django pattern used in ModelForms and authentication forms.

        model = User
        # This form is connected to Django's built-in User model.
        # When the form is saved, the data goes into the auth_user table in the database.

        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]
        # These are the fields shown on the registration form.
        # password1 and password2 come from UserCreationForm.
        # Django compares both passwords and only creates the user if they match and pass validation.
        # This supports the assignment requirement for user registration and secure login.


class UserUpdateForm(forms.ModelForm):
    """Allows the logged-in user to update basic account details."""
    # This form allows an existing logged-in user to update their basic User account details.
    # It is a ModelForm, meaning Django builds the form directly from the User model.
    # This avoids repeating model field definitions manually.

    class Meta:
        # The Meta class connects this form to a model and selects the editable fields.

        model = User
        # This form updates the built-in Django User model.
        # It affects the same auth_user table used for authentication.

        fields = ["first_name", "last_name", "email"]
        # These are the only User fields that can be updated through this form.
        # I do not include username or password here because changing those should be handled separately and more carefully.
        # This keeps the profile update page focused on safe account details.


class UserProfileUpdateForm(forms.ModelForm):
    """Allows users to update contact details without changing their own role."""
    # This form updates the extra profile information stored in the UserProfile model.
    # It is separated from UserUpdateForm because Django's User model and my UserProfile model are two different database tables.
    # The wider idea is: User = login identity, UserProfile = extra project-specific profile details.

    class Meta:
        # The Meta class tells Django which model this form edits and which fields are allowed.

        model = UserProfile
        # This connects the form to the UserProfile model.
        # The data from this form is stored in the accounts_userprofile table.

        fields = ["phone", "organisation", "job_title"]
        # These are the profile fields the user is allowed to edit.
        # The role field is intentionally not included here.
        # This is important because normal users should not be able to make themselves an Adviser, Portfolio Manager or Admin.
        # Role changes should be controlled through Django admin or protected staff-only logic.