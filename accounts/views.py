"""Account views for registration, profile updates and password reset demo flow."""

from django.contrib import messages
# This imports Django's messages framework.
# The messages framework is used to send one-time messages from the view to the template.

from django.contrib.auth import login
# This imports Django's login() function.
# login() connects a user object to the current browser session.

from django.contrib.auth.decorators import login_required
# This imports the login_required decorator.
# It protects pages so only authenticated users can access them.

from django.contrib.auth.forms import PasswordResetForm
# This imports Django's built-in password reset form.
# It checks whether the submitted email belongs to an active user with a usable password.

from django.contrib.auth.tokens import default_token_generator
# This imports Django's secure password reset token generator.
# It creates the token used inside the password reset link.

from django.shortcuts import redirect, render
# render() displays a template.
# redirect() sends the user to another page after an action is complete.

from django.utils.encoding import force_bytes
# force_bytes converts the user's database ID into bytes before encoding it for the reset URL.

from django.utils.http import urlsafe_base64_encode
# urlsafe_base64_encode safely encodes the user ID for use inside a URL.

from .forms import RegisterForm, UserProfileUpdateForm, UserUpdateForm
# This imports the custom forms used by the accounts app.


def register(request):
    # This view controls user registration.
    """Register a new user and log them in immediately."""

    if request.method == "POST":
        # This runs when the registration form is submitted.

        form = RegisterForm(request.POST)
        # This creates a form using the submitted registration data.

        if form.is_valid():
            # This checks whether the submitted data is valid.

            user = form.save()
            # This saves the new user account to the database.

            login(request, user)
            # This logs the new user in immediately after registration.

            messages.success(request, "Account created successfully. You can now complete your profile.")
            # This shows a success message after registration.

            return redirect("accounts:profile")
            # This redirects the user to their profile page.

    else:
        # This runs when the registration page is opened normally.

        form = RegisterForm()
        # This creates an empty registration form.

    return render(request, "registration/register.html", {"form": form})
    # This displays the registration page.


@login_required
def profile(request):
    # This view displays and updates the logged-in user's profile.
    """Display and update the logged-in user's personal/contact profile."""

    if request.method == "POST":
        # This runs when the profile form is submitted.

        user_form = UserUpdateForm(request.POST, instance=request.user)
        # This updates fields from Django's built-in User model.

        profile_form = UserProfileUpdateForm(request.POST, instance=request.user.profile)
        # This updates fields from the custom UserProfile model.

        if user_form.is_valid() and profile_form.is_valid():
            # Both forms must be valid before saving.

            user_form.save()
            # This saves the updated User model data.

            profile_form.save()
            # This saves the updated UserProfile model data.

            messages.success(request, "Your profile was updated successfully.")
            # This shows a success message after the profile is saved.

            return redirect("accounts:profile")
            # This redirects back to the profile page.

    else:
        # This runs when the profile page is opened normally.

        user_form = UserUpdateForm(instance=request.user)
        # This pre-fills the user form with the logged-in user's current details.

        profile_form = UserProfileUpdateForm(instance=request.user.profile)
        # This pre-fills the profile form with the user's current profile details.

    return render(
        request,
        "accounts/profile.html",
        {"user_form": user_form, "profile_form": profile_form}
    )
    # This displays the profile page with both forms.


def demo_password_reset(request):
    # This view creates a secure Django password reset link without using Gmail SMTP.
    # This is useful for the Render academic deployment because Gmail SMTP was causing the worker to crash.
    # The generated reset link is displayed on the next page instead of being emailed.

    if request.method == "POST":
        # This runs when the password reset form is submitted.

        form = PasswordResetForm(request.POST)
        # This uses Django's built-in password reset form.

        reset_link = None
        # This will store the generated password reset link if a matching user is found.

        if form.is_valid():
            # This checks whether the submitted email field is valid.

            email = form.cleaned_data["email"]
            # This gets the email address entered by the user.

            users = form.get_users(email)
            # This finds active users with that email address and a usable password.

            for user in users:
                # This loops through matching users.
                # Usually there should only be one user for one email address.

                uid = urlsafe_base64_encode(force_bytes(user.pk))
                # This safely encodes the user's primary key for the password reset URL.

                token = default_token_generator.make_token(user)
                # This creates Django's secure password reset token.

                reset_link = request.build_absolute_uri(
                    f"/accounts/reset/{uid}/{token}/"
                )
                # This builds the full Render URL for the password reset page.

                break
                # This stops after the first matching user.

        request.session["demo_password_reset_link"] = reset_link
        # This stores the reset link temporarily in the browser session.

        return redirect("accounts:password_reset_done")
        # This sends the user to the password reset done page.

    else:
        # This runs when the password reset page is opened normally.

        form = PasswordResetForm()
        # This creates an empty password reset form.

    return render(request, "registration/password_reset_form.html", {"form": form})
    # This displays the password reset form.


def demo_password_reset_done(request):
    # This view displays the password reset link generated by demo_password_reset.
    # This makes the password reset workflow reliable on Render for the assignment demonstration.

    reset_link = request.session.get("demo_password_reset_link")
    # This gets the reset link from the session.

    return render(
        request,
        "registration/password_reset_done.html",
        {"reset_link": reset_link}
    )
    # This displays the done page and sends the reset link to the template.