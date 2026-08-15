from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

def demo_password_reset(request):
    # This view creates a password reset link without using Gmail SMTP.
    # It is used for the deployed academic demonstration so the reset workflow works reliably on Render.

    reset_link = None
    # This variable will store the reset link after Django generates it.

    if request.method == "POST":
        # This checks if the user submitted the password reset form.

        form = PasswordResetForm(request.POST)
        # This uses Django's built-in password reset form, so the email validation still follows Django's normal workflow.

        if form.is_valid():
            # This checks that the submitted email field is valid.

            email = form.cleaned_data["email"]
            # This gets the email address entered by the user.

            users = form.get_users(email)
            # This finds active users with this email address and a usable password.

            for user in users:
                # This loops through matching users. Normally there should only be one user for the email.

                uid = urlsafe_base64_encode(force_bytes(user.pk))
                # This safely encodes the user's database ID for the reset URL.

                token = default_token_generator.make_token(user)
                # This creates Django's secure password reset token.

                reset_link = request.build_absolute_uri(
                    reverse_lazy(
                        "password_reset_confirm",
                        kwargs={"uidb64": uid, "token": token}
                    )
                )
                # This builds the full Render URL for the password reset confirmation page.

                break
                # This stops after the first matching user.

            request.session["demo_password_reset_link"] = reset_link
            # This stores the generated reset link temporarily in the user's browser session.

            return redirect("password_reset_done")
            # This redirects to the normal password reset done page.

    else:
        # This runs when the user opens the password reset page normally.

        form = PasswordResetForm()
        # This creates an empty password reset form.

    return render(request, "registration/password_reset_form.html", {"form": form})
    # This displays the password reset form template.


def demo_password_reset_done(request):
    # This view displays the generated reset link for the academic Render demo.

    reset_link = request.session.get("demo_password_reset_link")
    # This gets the reset link from the session.

    return render(
        request,
        "registration/password_reset_done.html",
        {"reset_link": reset_link}
    )
    # This sends the reset link to the template so it can be displayed.