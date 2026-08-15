from django.contrib import messages
# This imports Django's messages framework so success messages can be shown after registration or profile updates.

from django.contrib.auth import login
# This allows the system to automatically log in a user after registration.

from django.contrib.auth.decorators import login_required
# This protects profile pages so only logged-in users can access them.

from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
# UserCreationForm is used for registration.
# PasswordResetForm is used to find users by email and create a reset workflow.

from django.contrib.auth.tokens import default_token_generator
# This creates Django's secure password reset token.

from django.shortcuts import redirect, render
# These shortcuts are used to display templates and redirect users after actions.

from django.urls import reverse_lazy
# This safely reverses URL names, especially inside password reset logic.

from django.utils.encoding import force_bytes
# This converts the user ID into bytes before encoding it for the reset URL.

from django.utils.http import urlsafe_base64_encode
# This safely encodes the user ID for the password reset URL.

from .forms import UserProfileForm
# This imports the custom profile form from accounts/forms.py.


def register(request):
    # This view handles user registration.

    if request.method == "POST":
        # This checks whether the registration form was submitted.

        form = UserCreationForm(request.POST)
        # This creates a registration form using the submitted data.

        if form.is_valid():
            # This checks whether the submitted username and password are valid.

            user = form.save()
            # This saves the new user account to the database.

            login(request, user)
            # This automatically logs in the new user after registration.

            messages.success(request, "Account created successfully.")
            # This shows a success message after registration.

            return redirect("accounts:profile")
            # This sends the new user to the profile page.

    else:
        # This runs when the registration page is opened normally.

        form = UserCreationForm()
        # This creates an empty registration form.

    return render(request, "registration/register.html", {"form": form})
    # This displays the registration page.


@login_required
def profile(request):
    # This view displays and updates the logged-in user's profile.

    profile_obj = request.user.profile
    # This gets the profile linked to the logged-in user.

    if request.method == "POST":
        # This checks whether the profile form was submitted.

        form = UserProfileForm(request.POST, instance=profile_obj)
        # This creates a form using the submitted profile data.

        if form.is_valid():
            # This checks whether the profile data is valid.

            form.save()
            # This saves the updated profile to the database.

            messages.success(request, "Profile updated successfully.")
            # This shows a success message after the profile is saved.

            return redirect("accounts:profile")
            # This reloads the profile page after saving.

    else:
        # This runs when the profile page is opened normally.

        form = UserProfileForm(instance=profile_obj)
        # This creates a form pre-filled with the current profile data.

    return render(request, "accounts/profile.html", {"form": form})
    # This displays the profile page.


def demo_password_reset(request):
    # This view creates a password reset link without depending on Gmail SMTP.
    # It is suitable for the Render assignment demonstration because Gmail SMTP was causing worker crashes.

    reset_link = None
    # This will store the generated reset link if a matching user is found.

    if request.method == "POST":
        # This checks whether the password reset form was submitted.

        form = PasswordResetForm(request.POST)
        # This creates Django's built-in password reset form using the submitted email.

        if form.is_valid():
            # This checks that the submitted email field is valid.

            email = form.cleaned_data["email"]
            # This gets the email address entered by the user.

            users = form.get_users(email)
            # This finds active users with this email address and a usable password.

            for user in users:
                # This loops through matching users.

                uid = urlsafe_base64_encode(force_bytes(user.pk))
                # This safely encodes the user's database ID for the reset link.

                token = default_token_generator.make_token(user)
                # This creates Django's secure password reset token.

                reset_link = request.build_absolute_uri(
                    reverse_lazy(
                        "accounts:password_reset_confirm",
                        kwargs={"uidb64": uid, "token": token},
                    )
                )
                # This builds the full Render URL for the reset page.

                break
                # This stops after the first matching user.

            request.session["demo_password_reset_link"] = reset_link
            # This stores the reset link temporarily in the user's session.

            return redirect("accounts:password_reset_done")
            # This sends the user to the password reset done page.

    else:
        # This runs when the password reset page is opened normally.

        form = PasswordResetForm()
        # This creates an empty password reset form.

    return render(request, "registration/password_reset_form.html", {"form": form})
    # This displays the password reset form.


def demo_password_reset_done(request):
    # This view shows the generated reset link for the academic Render demonstration.

    reset_link = request.session.get("demo_password_reset_link")
    # This gets the reset link from the user's session.

    return render(
        request,
        "registration/password_reset_done.html",
        {"reset_link": reset_link},
    )
    # This displays the password reset done page and passes the link to the template.