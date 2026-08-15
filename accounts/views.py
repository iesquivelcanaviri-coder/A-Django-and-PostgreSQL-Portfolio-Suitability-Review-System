from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

def demo_password_reset(request):
    # This view creates a secure password reset link without relying on external email services.
    # It is used for the Render academic deployment so the password reset workflow works reliably.

    reset_link = None
    # This variable will store the generated password reset link.

    if request.method == "POST":
        # This runs when the user submits the password reset form.

        form = PasswordResetForm(request.POST)
        # This uses Django's built-in PasswordResetForm to validate the submitted email address.

        if form.is_valid():
            # This checks that the email field is valid.

            email = form.cleaned_data["email"]
            # This gets the email address entered by the user.

            users = form.get_users(email)
            # This finds active users with that email address and a usable password.

            for user in users:
                # This loops through matching users. Usually there should only be one matching user.

                uid = urlsafe_base64_encode(force_bytes(user.pk))
                # This safely encodes the user's database ID for the reset URL.

                token = default_token_generator.make_token(user)
                # This creates Django's secure password reset token.

                reset_path = reverse(
                    "accounts:password_reset_confirm",
                    kwargs={"uidb64": uid, "token": token},
                )
                # This creates the internal reset URL path.

                reset_link = request.build_absolute_uri(reset_path)
                # This creates the full Render URL for the password reset link.

                break
                # This stops after the first matching active user.

            request.session["demo_password_reset_link"] = reset_link
            # This stores the reset link temporarily in the browser session.

            return redirect("accounts:password_reset_done")
            # This sends the user to the reset confirmation page.

    else:
        # This runs when the user first opens the password reset page.

        form = PasswordResetForm()
        # This creates an empty password reset form.

    return render(request, "registration/password_reset_form.html", {"form": form})
    # This displays the password reset form.


def demo_password_reset_done(request):
    # This view displays the generated password reset link for the academic Render deployment.

    reset_link = request.session.get("demo_password_reset_link")
    # This retrieves the reset link from the browser session.

    return render(
        request,
        "registration/password_reset_done.html",
        {"reset_link": reset_link},
    )
    # This sends the reset link to the template.