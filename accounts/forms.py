"""Forms for registration and profile editing."""
# This short file description explains the purpose of forms.py in the accounts app.
# In this project, this file is responsible for the forms linked to user registration and profile editing.
# Django forms help connect the frontend templates, the database models and the validation process together.
from django import forms
# This imports Django's forms framework.
# I need this because Django provides ready-made form classes such as ModelForm, EmailField and CharField.
# Using Django forms means I do not need to manually write all HTML form fields and validation logic from scratch.
from django.contrib.auth.forms import UserCreationForm
# This imports Django's built-in UserCreationForm.
# UserCreationForm is designed for safely creating new user accounts.
# It already includes password fields, password confirmation and password validation.
# This is important because password handling should follow Django's security system instead of being coded manually.
from django.contrib.auth.models import User
# This imports Django's built-in User model.
# The User model is part of Django's authentication framework.
# It stores core account information such as username, first name, last name, email and password.
# In the database, this information is stored in Django's built-in auth_user table.
# This connects directly to login, logout, sessions and password security across the whole web app.
from .models import UserProfile
# This imports the UserProfile model from the current accounts app.
# The dot before models means Django should look inside the same app folder.
# UserProfile stores extra user details that are not included in Django's default User model.
# In this project, UserProfile is used for phone number, organisation, job title and role.
# This shows a wider Django pattern: use the built-in User model for authentication and a profile model for extra project-specific information.

class RegisterForm(UserCreationForm):
    # This creates a custom registration form for new users.
    # It inherits from UserCreationForm, so it automatically includes username, password1 and password2.
    # I am extending the built-in form by adding email, first name and last name.
    # This supports the assignment requirement for user registration and also makes the account records more complete.
    """Registration form using Django's secure built-in password handling."""
    email = forms.EmailField(required=True)
    # This creates an email field on the registration form.
    # required=True means the user must enter an email address before the form can be submitted.
    # Django will also check that the input looks like an email address.
    # This field will later be saved into the email column of the built-in User model.
    first_name = forms.CharField(max_length=150, required=True)
    # This creates a first name field on the registration form.
    # max_length=150 matches the maximum length used by Django's built-in User model.
    # required=True means the user must enter their first name during registration.
    # This makes the user account easier to identify in the dashboard, messages and admin panel.
    last_name = forms.CharField(max_length=150, required=True)
    # This creates a last name field on the registration form.
    # It also uses max_length=150 to stay consistent with Django's User model.
    # required=True means the user must provide a surname before the account can be created.
    # This is useful in a portfolio suitability system because different users may have different roles, such as client, adviser or reviewer.

    class Meta:
        # The Meta class gives Django extra instructions about the form.
        # In Django, Meta is commonly used to connect a form to a model and choose which model fields are included.
        # This keeps the form linked to the database structure instead of treating it as a completely separate HTML form.
        model = User
        # This tells Django that RegisterForm is connected to the built-in User model.
        # When the form is valid and saved, Django creates a new record in the auth_user database table.
        # This also connects the new user to Django's login and authentication system.
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]
        # This list controls which fields appear on the registration form.
        # username, first_name, last_name and email come from the User model.
        # password1 and password2 come from UserCreationForm.
        # Django checks that password1 and password2 match before creating the account.
        # This helps meet the assignment requirement for secure user registration.

class UserUpdateForm(forms.ModelForm):
    # This creates a form for updating the logged-in user's basic account details.
    # It inherits from forms.ModelForm, which means Django builds the form from a database model.
    # This form is connected to the built-in User model, not the UserProfile model.
    # The wider idea is that this form updates identity information, while UserProfileUpdateForm updates extra profile information.
    """Allows the logged-in user to update basic account details."""
    class Meta:
        # The Meta class tells Django which model this form edits and which fields should be included.
        # Without this Meta class, Django would not know which database model the form should connect to.
        model = User
        # This connects the form to Django's built-in User model.
        # Any saved changes from this form update the auth_user table.
        # This means the form is changing the same user account used for authentication.
        fields = ["first_name", "last_name", "email"]
        # These are the only fields from the User model that the user can update through this form.
        # I do not include username here because changing usernames can affect account identity and should be handled carefully.
        # I do not include password here because password changes should use Django's password reset or password change system.
        # This keeps the profile update form focused and safer.

class UserProfileUpdateForm(forms.ModelForm):
    # This creates a form for updating the extra profile details stored in the UserProfile model.
    # It is separate from UserUpdateForm because User and UserProfile are different models and different database tables.
    # This separation is a common Django design pattern.
    # User stores authentication details, while UserProfile stores project-specific information.
    """Allows users to update contact details without changing their own role."""
    class Meta:
        # The Meta class tells Django which model this form is connected to.
        # It also controls which fields the user is allowed to edit.
        # This is important for security because excluding a field from the form means the user cannot edit it through this page.
        model = UserProfile
        # This connects the form to the UserProfile model in the accounts app.
        # The data from this form is saved in the accounts_userprofile table.
        # This is where the app stores additional user information beyond Django's built-in User model.
        fields = ["phone", "organisation", "job_title"]
        # These are the only UserProfile fields that normal users can update.
        # phone allows the user to store a contact number.
        # organisation allows the user to record the company, institution or department they belong to.
        # job_title allows the user to describe their role in the portfolio suitability workflow.
        # The role field is deliberately not included here.
        # This prevents users from giving themselves higher permissions, such as Adviser, Portfolio Manager, Compliance Reviewer or Admin.
        # Role changes should be controlled by an administrator or by protected staff-only logic.