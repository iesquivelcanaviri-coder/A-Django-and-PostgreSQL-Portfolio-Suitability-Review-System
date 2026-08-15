from django.contrib.auth import login
# login signs in the user automatically after successful registration.

from django.contrib.auth.decorators import login_required
# login_required protects private pages such as the profile page.

from django.contrib.auth.forms import PasswordResetForm, UserCreationForm
# UserCreationForm is used for registration, and PasswordResetForm is used for reset email lookup.

from django.contrib.auth.tokens import default_token_generator
# This creates Django's secure password reset token.

from django.shortcuts import redirect, render
# render displays templates, and redirect sends the user to another page.

from django.urls import reverse_lazy
# reverse_lazy builds URL names safely.

from django.utils.encoding import force_bytes
# force_bytes converts the user primary key before encoding it.

from django.utils.http import urlsafe_base64_encode
# This safely encodes the user ID for the password reset URL.

from .forms import UserProfileForm
# This imports your profile form from accounts/forms.py.


def register(request):
    # This view handles new user registration.

    if request.method == "POST":
        # This checks whether the user submitted the registration form.

        form = UserCreationForm(request.POST)
        # This creates a Django registration form using the submitted data.

        if form.is_valid():
            # This checks that the submitted username and passwords are valid.

            user = form.save()
            # This saves the new user to the database.

            login(request, user)
            # This logs the user in immediately after registration.

            return redirect("accounts:profile")
            # This sends the new user to the profile page.

    else:
        # This runs when the user opens the registration page normally.

        form = UserCreationForm()
        # This creates an empty registration form.

    return render(request, "registration/register.html", {"form": form})
    # This displays the registration page.


@login_required
def profile(request):
    # This view allows a logged-in user to view or update their profile.

    profile = request.user.profile
    # This gets the profile connected to the logged-in user.

    if request.method == "POST":
        # This checks whether the profile form was submitted.

        form = UserProfileForm(request.POST, instance=profile)
        # This binds the submitted data to the existing profile record.

        if form.is_valid():
            # This checks whether the submitted profile data is valid.

            form.save()
            # This saves the updated profile.

            return redirect("accounts:profile")
            # This reloads the profile page after saving.

    else:
        # This runs when the user opens the profile page normally.

        form = UserProfileForm(instance=profile)
        # This displays the existing profile details in the form.

    return render(request, "accounts/profile.html", {"form": form})
    # This displays the profile page.


def demo_password_reset(request):
    # This view creates a password reset link without relying on Gmail SMTP.
    # It is used for the deployed academic demonstration on Render.

    reset_link = None
    # This will store the generated password reset link.

    if request.method == "POST":
        # This checks whether the reset form was submitted.

        form = PasswordResetForm(request.POST)
        # This uses Django's built-in password reset form.

        if form.is_valid():
            # This validates the email field.

            email = form.cleaned_data["email"]
            # This gets the submitted email address.

            users = form.get_users(email)
            # This finds active users with that email and a usable password.

            for user in users:
                # This loops through matching users.

                uid = urlsafe_base64_encode(force_bytes(user.pk))
                # This encodes the user's database ID for the reset URL.

                token = default_token_generator.make_token(user)
                # This creates Django's secure reset token.

                reset_link = request.build_absolute_uri(
                    reverse_lazy(
                        "accounts:password_reset_confirm",
                        kwargs={"uidb64": uid, "token": token},
                    )
                )
                # This builds the full Render password reset link.

                break
                # This stops after the first matching user.

            request.session["demo_password_reset_link"] = reset_link
            # This stores the reset link temporarily in the user's session.

            return redirect("accounts:password_reset_done")
            # This redirects to the done page where the link can be displayed.

    else:
        # This runs when the reset page is opened normally.

        form = PasswordResetForm()
        # This creates an empty password reset form.

    return render(request, "registration/password_reset_form.html", {"form": form})
    # This displays the password reset form.


def demo_password_reset_done(request):
    # This view displays the generated reset link for the academic Render demo.

    reset_link = request.session.get("demo_password_reset_link")
    # This gets the reset link from the session.

    return render(
        request,
        "registration/password_reset_done.html",
        {"reset_link": reset_link},
    )
    # This displays the done page with the reset link.