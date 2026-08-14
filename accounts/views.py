from django.contrib.auth.forms import PasswordResetForm
# This imports Django's built-in password reset form.

from django.contrib.auth.tokens import default_token_generator
# This imports Django's secure password reset token generator.

from django.shortcuts import redirect, render
# render displays templates, and redirect sends the user to another page.

from django.urls import reverse
# reverse builds URLs from Django route names.

from django.utils.encoding import force_bytes
# force_bytes converts the user ID into bytes before encoding it safely.

from django.utils.http import urlsafe_base64_encode
# urlsafe_base64_encode creates the encoded user ID used inside the reset URL.



def demo_password_reset(request):
    # This view creates a secure password reset link without using Gmail SMTP.
    # It is used for the Render academic deployment so the password reset workflow works reliably.

    reset_link = None
    # This variable will store the generated reset link if a matching user is found.

    if request.method == "POST":
        # This checks whether the user submitted the password reset form.

        form = PasswordResetForm(request.POST)
        # This uses Django's built-in password reset form to validate the submitted email address.

        if form.is_valid():
            # This checks whether the email field is valid.

            email = form.cleaned_data["email"]
            # This gets the email address entered by the user.

            users = form.get_users(email)
            # This finds active users with this email address and a usable password.
            # This keeps Django's normal password reset user-checking behaviour.

            for user in users:
                # This loops through matching users. Usually there should only be one.

                uid = urlsafe_base64_encode(force_bytes(user.pk))
                # This safely encodes the user's database ID for the reset URL.

                token = default_token_generator.make_token(user)
                # This creates Django's secure password reset token.

                reset_link = request.build_absolute_uri(
                    reverse(
                        "accounts:password_reset_confirm",
                        kwargs={"uidb64": uid, "token": token},
                    )
                )
                # This builds the full Render URL for the password reset confirmation page.

                break
                # This stops after the first matching user.

            request.session["demo_password_reset_link"] = reset_link
            # This stores the generated link temporarily in the user's session.

            return redirect("accounts:password_reset_done")
            # This sends the user to the done page where the link can be displayed.

    else:
        # This runs when the user first opens the password reset page.

        form = PasswordResetForm()
        # This creates an empty password reset form.

    return render(request, "registration/password_reset_form.html", {"form": form})
    # This displays the password reset form template.


def demo_password_reset_done(request):
    # This view shows the generated password reset link for the academic Render demo.

    reset_link = request.session.get("demo_password_reset_link")
    # This retrieves the reset link from the user's session.

    return render(
        request,
        "registration/password_reset_done.html",
        {"reset_link": reset_link},
    )
    # This sends the reset link to the template so it can be displayed on the page.