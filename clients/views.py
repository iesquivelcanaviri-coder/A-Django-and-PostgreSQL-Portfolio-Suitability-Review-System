"""Views for client profile, financial profile and risk assessment CRUD."""
from django.contrib import messages
# Imports Django's messages framework, which lets the view send success or error messages to the template after an action.
from django.contrib.auth.decorators import login_required
# Imports the login_required decorator so only logged-in users can access these views.
from django.shortcuts import get_object_or_404, redirect, render
# Imports useful Django shortcut functions:render displays a template, redirect sends the user to another URL, and get_object_or_404 gets a database object or shows a 404 page.
from .forms import ClientProfileForm, FinancialProfileForm, RiskAssessmentForm
# Imports the forms from this app so the user can create or update client, financial and risk assessment data through HTML forms.
from .models import ClientProfile, FinancialProfile, RiskAssessment
# Imports the database models used in this file.
# These models connect the view logic to the PostgreSQL database through Django's ORM.

@login_required
# This means the user must be logged in before they can view the client list page.
# If the user is not logged in, Django redirects them to the login page.
def client_list(request):
    # Defines the client_list view function.
    # The request object contains information about the current browser request, including the logged-in user.
    """Show all client records visible to logged-in users for the prototype."""
    clients = ClientProfile.objects.select_related("financial_profile").all()
    # Gets all client profile records from the database.
    # select_related("financial_profile") is used to also fetch the linked financial profile in the same database query.
    # This is more efficient than querying the financial profile separately for every client.
    return render(request, "clients/client_list.html", {"clients": clients})
    # Sends the user to the clients/client_list.html template.
    # The dictionary {"clients": clients} passes the client records into the template so they can be displayed on the page.

@login_required
# Protects the client creation page so only logged-in users can create client profiles.
def client_create(request):
    # Defines the view that handles creating a new client profile.
    # This view handles both showing the blank form and processing the submitted form.
    """Create a new client profile record."""
    if request.method == "POST":
        # Checks whether the form has been submitted.
        # In Django, POST usually means the user clicked submit and sent form data to the server.
        form = ClientProfileForm(request.POST)
        # Creates a form object using the submitted data from the request.
        # request.POST contains the values typed into the HTML form.
        if form.is_valid():
            # Checks whether the submitted form passes Django's validation rules.
            # This includes required fields, correct data types and any custom validation in the form or model.
            client = form.save(commit=False)
            # Creates a ClientProfile object from the form but does not save it to the database yet.
            # commit=False is useful because we still need to add extra data that is not typed directly into the form.
            client.created_by = request.user
            # Stores the logged-in user as the person who created this client record.
            # request.user comes from Django's authentication system.
            client.save()
            # Saves the completed client profile object to the database.
            messages.success(request, "Client profile created.")
            # Adds a success message that can be displayed on the next page.
            # This gives the user feedback that the client profile was created successfully.
            return redirect("clients:detail", pk=client.pk)
            # Redirects the user to the detail page for the new client.
            # client.pk is the primary key of the new database record.
            # "clients:detail" connects to the named URL pattern in clients/urls.py.
    else:
        # Runs when the request is not POST.
        # Usually this means the user is opening the page for the first time with a GET request.
        form = ClientProfileForm()
        # Creates a blank client profile form for the user to fill in.
    return render(request, "clients/client_form.html", {"form": form, "title": "Create Client Profile"})
    # Displays the form template.
    # The form variable is passed into the template so Django can render the form fields.
    # The title variable lets the same template show a page heading for creating a client.


@login_required
# Protects the client detail page so only logged-in users can view client records.
def client_detail(request, pk):
    # Defines the view for reading one specific client profile.
    # pk means primary key, which identifies the exact client record in the database.
    """Read one client profile with financial, risk and mandate context."""
    client = get_object_or_404(ClientProfile, pk=pk)
    # Tries to get the client profile with the matching primary key.
    # If no matching client exists, Django automatically shows a 404 not found page.
    # This is safer than using ClientProfile.objects.get() without error handling.
    return render(request, "clients/client_detail.html", {"client": client})
    # Displays the client_detail.html template.
    # The selected client object is passed into the template so its fields and related records can be shown.

@login_required
# Protects the update page so only logged-in users can edit a client profile.
def client_update(request, pk):
    # Defines the view for updating an existing client profile.
    # The pk identifies which client record should be edited.
    """Update an existing client profile."""
    client = get_object_or_404(ClientProfile, pk=pk)
    # Gets the existing client record from the database.
    # If the record does not exist, Django returns a 404 page instead of crashing.
    if request.method == "POST":
        # Checks whether the user submitted the edit form.
        form = ClientProfileForm(request.POST, instance=client)
        # Creates a form using the submitted data and connects it to the existing client object.
        # instance=client tells Django this is an update, not a new record.
        if form.is_valid():
            # Checks that the updated information is valid before saving it.
            form.save()
            # Saves the changes to the existing client profile in the database.
            messages.success(request, "Client profile updated.")
            # Shows a success message after the update is saved.
            return redirect("clients:detail", pk=client.pk)
            # Redirects back to the client detail page after the update.
            # This follows the common POST-Redirect-GET pattern, which avoids duplicate form submissions.
    else:
        # Runs when the user first opens the update page with a GET request.
        form = ClientProfileForm(instance=client)
        # Creates a form pre-filled with the existing client data.
        # This lets the user see and edit the current values.
    return render(request, "clients/client_form.html", {"form": form, "title": "Update Client Profile"})
    # Displays the same client_form.html template used for creating a client.
    # Reusing the template keeps the project more modular and avoids duplicate HTML.

@login_required
# Protects the financial profile page so only logged-in users can create or update financial information.
def financial_profile_edit(request, client_pk):
    # Defines the view for creating or editing the financial profile linked to one client.
    # client_pk identifies which client the financial profile belongs to.
    """Create or update the financial profile linked to a client."""
    client = get_object_or_404(ClientProfile, pk=client_pk)
    # Gets the client record linked to the financial profile.
    # If the client does not exist, Django returns a 404 page.
    profile, _created = FinancialProfile.objects.get_or_create(client=client)
    # Gets the financial profile for this client if it already exists. If it does not exist, Django creates one automatically.
    # The _created variable tells whether a new profile was created, but it is not used later, so the underscore shows it is intentionally ignored.
    if request.method == "POST":
        # Checks whether the user submitted the financial profile form.
        form = FinancialProfileForm(request.POST, instance=profile)
        # Creates a form from the submitted data and links it to the financial profile object.
        # Because instance=profile is used, Django updates the existing profile instead of creating a duplicate.
        if form.is_valid():
            # Validates the financial profile data before saving it.
            form.save()
            # Saves the financial profile to the database.
            messages.success(request, "Financial profile saved.")
            # Shows a success message confirming that the financial profile was saved.
            return redirect("clients:detail", pk=client.pk)
            # Redirects back to the client detail page.
            # This lets the user immediately see the updated client and financial information.
    else:
        # Runs when the user opens the financial profile form for the first time.
        form = FinancialProfileForm(instance=profile)
        # Creates a form pre-filled with the financial profile data.
        # If the profile was newly created, the form will mostly be blank.
    return render(request, "clients/client_form.html", {"form": form, "title": "Financial Profile"})
    # Reuses the client_form.html template to display the financial profile form.
    # The title helps the template show the correct heading for this page.

@login_required
# Protects the risk assessment creation page so only logged-in users can create risk assessments.
def risk_assessment_create(request):
    # Defines the view for creating a new risk assessment.
    # This view links the submitted assessment to the logged-in user as assessor.
    """Create a risk assessment and automatically calculate the outcome."""
    if request.method == "POST":
        # Checks whether the user submitted the risk assessment form.
        form = RiskAssessmentForm(request.POST)
        # Creates a risk assessment form using the submitted form data.
        if form.is_valid():
            # Checks whether the submitted assessment data is valid.
            assessment = form.save(commit=False)
            # Creates a RiskAssessment object from the form but does not save it yet.
            # commit=False is needed because assessed_by is not entered by the user in the form.
            assessment.assessed_by = request.user
            # Stores the currently logged-in user as the person who completed the risk assessment.
            # This creates an audit-style link between the user and the assessment.
            assessment.save()
            # Saves the completed risk assessment to the database.
            # If the model has custom save logic, this may also calculate the suitability outcome.
            messages.success(request, f"Risk assessment saved: {assessment.get_outcome_display()}.")
            # Shows a success message that includes the readable version of the outcome.
            # get_outcome_display() is a Django method used when a model field has choices.
            return redirect("clients:detail", pk=assessment.client.pk)
            # Redirects the user back to the detail page for the client linked to the assessment.
            # assessment.client.pk gets the primary key of the related client.
    else:
        # Runs when the user first opens the risk assessment form.
        form = RiskAssessmentForm()
        # Creates a blank risk assessment form.
    return render(request, "clients/risk_form.html", {"form": form})
    # Displays the risk_form.html template.
    # The form is passed into the template so the user can complete the risk assessment.