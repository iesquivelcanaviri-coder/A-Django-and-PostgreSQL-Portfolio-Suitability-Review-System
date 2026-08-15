from django import forms
# This imports Django's forms module so the registration form can include an email field.

from django.contrib import messages
# This imports Django's messages framework so success messages can be shown after registration or profile updates.

from django.contrib.auth import get_user_model, login
# get_user_model gets the active Django user model, and login logs the user in after registration.

from django.contrib.auth.decorators import login_required
# This protects the profile page so only logged-in users can access it.

from django.contrib.auth.forms import PasswordResetForm, UserCreationForm
# PasswordResetForm is used to validate the email field.
# UserCreationForm is used as the base form for creating new users.

from django.contrib.auth.tokens import default_token_generator
# This imports Django's secure password reset token generator.

from django.shortcuts import redirect, render
# render displays templates, and redirect sends the user to another page.

from django.urls import reverse
# reverse builds a URL from a named URL pattern.

from django.utils.encoding import force_bytes
# force_bytes converts the user ID into bytes before it is encoded safely for the URL.

from django.utils.http import urlsafe_base64_encode
# This safely encodes the user ID for the reset link.


User = get_user_model()
# This stores the active Django user model in a variable.


class RegistrationForm(UserCreationForm):
    # This custom registration form extends Django's built-in UserCreationForm.

    email = forms.EmailField(required=True)
    # This adds an email field to registration, which is needed for password reset.

    class Meta:
        # The Meta class tells Django which model and fields to use.

        model = User
        # This connects the form to Django's user model.

        fields = ("username", "email", "password1", "password2")
        # These fields appear on the registration form.

    def save(self, commit=True):
        # This saves the new user and stores their email address.

        user = super().save(commit=False)
        # This creates the user object but does not save it yet.

        user.email = self.cleaned_data["email"]
        # This copies the submitted email into the user email field.

        if commit:
            # This checks whether Django should save the user to the database now.

            user.save()
            # This saves the new user account.

        return user
        # This returns the created user object.


def register(request):
    # This view handles new user registration.

    if request.method == "POST":
        # This runs when the user submits the registration form.

        form = RegistrationForm(request.POST)
        # This creates the custom registration form using the submitted data.

        if form.is_valid():
            # This checks whether the registration form is valid.

            user = form.save()
            # This saves the new user, including their email address.

            login(request, user)
            # This logs in the new user immediately after registration.

            messages.success(request, "Account created successfully.")
            # This shows a success message.

            return redirect("accounts:profile")
            # This sends the new user to their profile page.

    else:
        # This runs when the user first opens the registration page.

        form = RegistrationForm()
        # This creates a blank registration form.

    return render(request, "registration/register.html", {"form": form})
    # This renders the registration page.


@login_required
def profile(request):
    # This view displays the logged-in user's profile page.

    return render(request, "accounts/profile.html")
    # This renders the profile template.


def demo_password_reset(request):
    # This view creates a secure password reset link without using Gmail SMTP.
    # It is designed for the deployed academic Render demonstration.

    reset_link = None
    # This variable will store the generated reset link.

    email_submitted = None
    # This stores the email address entered by the user.

    if request.method == "POST":
        # This runs when the user submits the password reset form.

        form = PasswordResetForm(request.POST)
        # This uses Django's built-in password reset form for email validation.

        if form.is_valid():
            # This checks that the submitted email address is valid.

            email_submitted = form.cleaned_data["email"]
            # This gets the email address entered by the user.

            users = form.get_users(email_submitted)
            # This finds active users with this email address and a usable password.

            for user in users:
                # This loops through matching users.

                uid = urlsafe_base64_encode(force_bytes(user.pk))
                # This creates the encoded user ID for the reset URL.

                token = default_token_generator.make_token(user)
                # This creates Django's secure reset token for the user.

                reset_path = reverse(
                    "password_reset_confirm",
                    kwargs={"uidb64": uid, "token": token}
                )
                # This builds the path for Django's built-in password reset confirmation page.

                reset_link = request.build_absolute_uri(reset_path)
                # This creates the full Render URL for the reset link.

                break
                # This stops after the first matching user.

            request.session["demo_password_reset_link"] = reset_link
            # This stores the generated reset link in the user's session.

            request.session["demo_password_reset_email"] = email_submitted
            # This stores the submitted email in the session for display on the done page.

            return redirect("accounts:password_reset_done")
            # This redirects to the custom password reset done page.

    else:
        # This runs when the user first opens the reset page.

        form = PasswordResetForm()
        # This creates a blank password reset form.

    return render(request, "registration/password_reset_form.html", {"form": form})
    # This displays the password reset form.


def demo_password_reset_done(request):
    # This view displays the generated reset link for the academic Render demo.

    reset_link = request.session.get("demo_password_reset_link")
    # This gets the reset link from the session.

    email_submitted = request.session.get("demo_password_reset_email")
    # This gets the submitted email from the session.

    return render(
        request,
        "registration/password_reset_done.html",
        {
            "reset_link": reset_link,
            "email_submitted": email_submitted,
        }
    )
    # This sends the reset link and email to the template.