"""Account views for registration and profile updates."""
from django.contrib import messages
# This imports Django's messages framework.
# The messages framework is used to send one-time messages from the view to the template.
# For example, after a user registers or updates their profile, we can show a success message on the page.
from django.contrib.auth import login
# This imports Django's login() function.
# login() connects a user object to the current browser session.
# This means the user becomes logged in without needing to manually enter their username and password again.
from django.contrib.auth.decorators import login_required
# This imports the login_required decorator.
# A decorator is a function that adds extra behaviour to another function.
# Here, login_required protects a page so only authenticated users can access it.
from django.shortcuts import redirect, render
# This imports Django shortcut functions.
# render() combines a template with context data and returns an HTML response to the browser.
# redirect() sends the user to another URL after an action is complete.
from .forms import RegisterForm, UserProfileUpdateForm, UserUpdateForm
# This imports the custom form classes from the accounts app's forms.py file.
# RegisterForm is used to create a new user account.
# UserUpdateForm is used to update fields from Django's built-in User model.
# UserProfileUpdateForm is used to update extra profile/contact details from the custom UserProfile model.

def register(request):
    # This defines the register view function.
    # The request parameter contains information about the browser request, including the method, user and submitted form data.
    # This view controls what happens when someone opens or submits the registration page.
    """Register a new user and log them in immediately."""
    if request.method == "POST":
        # This checks whether the browser submitted the registration form.
        # In Django, a POST request usually means the user is sending data to the server.
        # For example, registration forms, login forms and profile update forms usually use POST.
        form = RegisterForm(request.POST)
        # This creates a RegisterForm object using the submitted form data.
        # request.POST contains the values typed into the form fields.
        # At this point, the form has data, but it has not been saved to the database yet.
        if form.is_valid():
            # This checks whether the form data passes Django's validation rules.
            # Validation can check things such as required fields, password rules, username rules and email format.
            # This is important because we should never save invalid user input directly into the database.
            user = form.save()
            # This saves the new user account to the database.
            # The saved user object is stored in the user variable.
            # This is useful because we need the user object in order to log the person in immediately.
            login(request, user)
            # This logs the newly registered user into the current session.
            # It means the user does not have to register first and then log in separately.
            # Django now treats this browser session as authenticated.
            messages.success(request, "Account created successfully. You can now complete your profile.")
            # This creates a success message for the user.
            # The message will usually appear on the next page if base.html displays messages.
            # This improves user experience because the user gets confirmation that registration worked.
            return redirect("accounts:profile")
            # This redirects the user to the profile page after successful registration.
            # "accounts:profile" uses Django's namespaced URL system.
            # "accounts" is the app namespace, and "profile" is the URL name inside accounts/urls.py.
            # This is better than hardcoding a URL like "/accounts/profile/" because named URLs are easier to maintain.
    else:
        # This else block runs when the request is not POST.
        # Usually this means the user opened the registration page normally using a GET request.
        # In that case, Django should display an empty form instead of trying to process submitted data.
        form = RegisterForm()
        # This creates a blank registration form.
        # The blank form is sent to the template so the user can fill it in.
    return render(request, "registration/register.html", {"form": form})
    # This renders the registration template and returns it to the browser.
    # "registration/register.html" is the HTML template file used for the registration page.
    # {"form": form} is the context dictionary.
    # The context sends the form variable from Python into the template so it can be displayed using Django template syntax.


@login_required
# This decorator protects the profile view.
# If a user is not logged in, Django will redirect them to the login page.
# This is important because profile details should not be visible or editable by anonymous visitors.
def profile(request):
    # This defines the profile view function.
    # This view displays and updates the logged-in user's profile information.
    # It works with two forms because the project uses both Django's built-in User model and a custom UserProfile model.
    """Display and update the logged-in user's personal/contact profile."""
    if request.method == "POST":
        # This checks whether the user submitted the profile update form.
        # POST means the browser is sending changed form data back to Django.
        user_form = UserUpdateForm(request.POST, instance=request.user)
        # This creates a UserUpdateForm using the submitted data.
        # request.POST contains the new values typed into the form.
        # instance=request.user tells Django to update the current logged-in user instead of creating a new user.
        # This form usually handles built-in user fields such as username, first name, last name or email.
        profile_form = UserProfileUpdateForm(request.POST, instance=request.user.profile)
        # This creates a UserProfileUpdateForm using the submitted data.
        # instance=request.user.profile tells Django to update the profile linked to the current user.
        # This works because the UserProfile model is connected to Django's User model, usually with a OneToOneField.
        # This form usually handles extra details such as phone number, organisation, job title or role.
        if user_form.is_valid() and profile_form.is_valid():
            # This checks that both forms are valid before saving.
            # Both forms need to be valid because the page updates data in two connected database tables.
            # This prevents a situation where one part of the profile saves successfully and the other part contains invalid data.
            user_form.save()
            # This saves the updated built-in User model fields to the database.
            # For example, this may update the user's username, first name, last name or email address.
            profile_form.save()
            # This saves the updated custom UserProfile fields to the database.
            # For example, this may update the user's phone number, organisation, job title or role.
            messages.success(request, "Your profile was updated successfully.")
            # This creates a success message after the profile update is saved.
            # The message can be displayed in the template to confirm that the update worked.
            return redirect("accounts:profile")
            # This redirects the user back to the profile page after saving.
            # This follows the POST-Redirect-GET pattern.
            # That pattern helps prevent duplicate form submissions if the user refreshes the browser after saving.
    else:
        # This else block runs when the request is not POST.
        # Usually this means the user opened the profile page normally using a GET request.
        # In that case, Django should show the existing saved profile details.
        user_form = UserUpdateForm(instance=request.user)
        # This creates a UserUpdateForm already filled with the current user's existing data.
        # instance=request.user tells the form which database record to display.
        profile_form = UserProfileUpdateForm(instance=request.user.profile)
        # This creates a UserProfileUpdateForm already filled with the current user's profile data.
        # request.user.profile gets the UserProfile object linked to the logged-in user.
    return render(request, "accounts/profile.html", {"user_form": user_form, "profile_form": profile_form})
    # This renders the profile page template and returns it to the browser.
    # "accounts/profile.html" is the HTML file used to display the profile update page.
    # The context dictionary sends both forms into the template.
    # user_form is used for Django's built-in User fields.
    # profile_form is used for the extra custom profile fields.
    
    
    