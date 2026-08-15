from django.contrib import messages
# Imports Django's messages framework so the app can show success messages after registration or profile updates.

from django.contrib.auth import login
# Imports Django's login function so the user can be logged in automatically after registration.

from django.contrib.auth.decorators import login_required
# Imports login_required so the profile page is protected from anonymous users.

from django.contrib.auth.forms import UserCreationForm
# Imports Django's built-in registration form.

from django.shortcuts import redirect, render
# Imports render for showing templates and redirect for sending users to another page after form submission.


def register(request):
    # This view handles new user registration.

    if request.method == "POST":
        # This runs when the user submits the registration form.

        form = UserCreationForm(request.POST)
        # This creates a registration form using the submitted data.

        if form.is_valid():
            # This checks whether the submitted registration data is valid.

            user = form.save()
            # This saves the new user account to the database.

            login(request, user)
            # This logs in the new user immediately after registration.

            messages.success(request, "Account created successfully.")
            # This shows a success message after registration.

            return redirect("accounts:profile")
            # This sends the user to their profile page after registration.

    else:
        # This runs when the user opens the registration page normally.

        form = UserCreationForm()
        # This creates a blank registration form.

    return render(request, "registration/register.html", {"form": form})
    # This renders the registration template and sends the form to the page.


@login_required
def profile(request):
    # This view displays the logged-in user's profile page.

    return render(request, "accounts/profile.html")
    # This renders the profile template.