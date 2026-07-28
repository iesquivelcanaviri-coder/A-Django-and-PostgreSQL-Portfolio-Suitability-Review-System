"""Views for mandate, holdings and portfolio review project CRUD."""
from django.contrib import messages
# Imports Django's messages framework, which lets us show success/error messages to the user after an action.
from django.contrib.auth.decorators import login_required
# Imports the login_required decorator, which protects a view so only logged-in users can access it.
from django.core.exceptions import PermissionDenied
# Imports PermissionDenied so we can block users who do not have the correct role or permission.
from django.shortcuts import get_object_or_404, redirect, render
# Imports common Django shortcuts:
# render displays a template, redirect sends the user to another page, and get_object_or_404 finds an object or shows a 404 page.
from .forms import HoldingForm, InvestmentMandateForm, ReviewProjectForm
# Imports the forms used to create and update holdings, investment mandates and review projects.
# These forms connect user input from HTML pages to Django model fields.
from .models import AuditLog, InvestmentMandate, PortfolioHolding, PortfolioReviewProject
# Imports the database models used in this file.
# These models represent database tables in PostgreSQL through Django's ORM.

def log_action(user, action, instance, description=""):
    # Defines a helper function used to record important user actions in the audit log.
    # This avoids repeating the same AuditLog.objects.create code in every view.
    """Save a small audit log row for important workflow actions."""
    AuditLog.objects.create(
        # Creates a new AuditLog row in the database using Django's ORM.
        user=user,
        # Stores which logged-in user performed the action.
        action=action,
        # Stores a short label for what happened, such as "Created mandate" or "Approved mandate".
        model_name=instance.__class__.__name__,
        # Stores the model class name of the object affected.
        # For example, if the object is an InvestmentMandate, this saves "InvestmentMandate".
        object_id=instance.pk,
        # Stores the primary key of the object affected.
        # This helps trace the audit log back to the exact database record.
        description=description
        # Stores any extra detail about the action.
        # The default is blank, but it can be used for more specific notes.
    )

@login_required
# This protects the mandate list page so only authenticated users can view it.
def mandate_list(request):
    # Defines the view that displays all investment mandates.
    mandates = InvestmentMandate.objects.select_related("client", "approved_by").all()
    # Gets all InvestmentMandate records from the database.
    # select_related is used for efficiency because client and approved_by are related objects.
    # This reduces extra database queries when the template displays client or approval information.
    return render(request, "mandates/mandate_list.html", {"mandates": mandates})
    # Renders the mandate_list.html template and sends the mandates queryset to the template.
    # The template can then loop through mandates and display them in a table or list.


@login_required
# This means only logged-in users can create an investment mandate.
def mandate_create(request):
    # Defines the view used to create a new investment mandate.
    if request.method == "POST":
        # Checks whether the user submitted the form.
        # POST means data was sent from the browser to the server.
        form = InvestmentMandateForm(request.POST)
        # Creates a form object using the submitted data from the request.
        if form.is_valid():
            # Checks if the submitted form data passes Django validation rules.
            mandate = form.save(commit=False)
            # Creates a mandate object from the form but does not save it to the database yet.
            # commit=False is useful because we still need to add created_by before saving.
            mandate.created_by = request.user
            # Records the logged-in user as the person who created the mandate.
            mandate.save()
            # Saves the completed mandate record to the PostgreSQL database.
            log_action(request.user, "Created mandate", mandate)
            # Adds an audit log entry so there is evidence that this user created the mandate.
            messages.success(request, "Investment mandate created.")
            # Shows a success message to the user after the mandate is created.
            return redirect("mandates:detail", pk=mandate.pk)
            # Redirects the user to the mandate detail page for the new mandate.
            # The pk is passed so Django knows exactly which mandate to show.
    else:
        # Runs when the page is opened normally with a GET request.
        # GET means the user is just viewing the blank form, not submitting it yet.
        form = InvestmentMandateForm()
        # Creates an empty form for the user to fill in.
    return render(
        # Renders the create/update mandate form page.
        request,
        # Passes the current HTTP request to the template.
        "mandates/mandate_form.html",
        # Tells Django which HTML template to use.
        {"form": form, "title": "Create Investment Mandate"}
        # Sends the form and page title into the template context.
    )

@login_required
# This protects the mandate detail page so only logged-in users can view it.
def mandate_detail(request, pk):
    # Defines the view used to show one specific mandate.
    # pk means primary key, which identifies the exact mandate record.
    mandate = get_object_or_404(InvestmentMandate, pk=pk)
    # Looks for the InvestmentMandate with the matching primary key.
    # If it does not exist, Django returns a 404 page instead of crashing.
    return render(request, "mandates/mandate_detail.html", {"mandate": mandate})
    # Renders the detail page and passes the selected mandate to the template.

@login_required
# This means only logged-in users can update an investment mandate.
def mandate_update(request, pk):
    # Defines the view used to edit an existing investment mandate.
    mandate = get_object_or_404(InvestmentMandate, pk=pk)
    # Finds the mandate being edited.
    # If the mandate does not exist, Django shows a 404 page.
    if request.method == "POST":
        # Checks whether the user has submitted the update form.
        form = InvestmentMandateForm(request.POST, instance=mandate)
        # Creates a form using the submitted data and links it to the existing mandate.
        # instance=mandate tells Django this is an update, not a new record.
        if form.is_valid():
            # Checks if the updated data is valid before saving.
            mandate = form.save()
            # Saves the updated mandate to the database.
            log_action(request.user, "Updated mandate", mandate)
            # Records the update in the audit log for accountability.
            messages.success(request, "Investment mandate updated.")
            # Shows a success message to the user.
            return redirect("mandates:detail", pk=mandate.pk)
            # Redirects back to the updated mandate detail page.
    else:
        # Runs when the user first opens the update page with a GET request.
        form = InvestmentMandateForm(instance=mandate)
        # Creates a form already filled with the current mandate values.
    return render(
        # Renders the mandate form template.
        request,
        # Sends the request object to the template.
        "mandates/mandate_form.html",
        # Uses the same template as mandate_create to avoid repeating HTML.
        {"form": form, "title": "Update Investment Mandate"}
        # Sends the form and title to the template.
    )

@login_required
# Only logged-in users can attempt to approve a mandate.
def mandate_approve(request, pk):
    # Defines the view used to approve an investment mandate.
    """Approve a mandate only when the user has a portfolio/compliance role."""
    # This docstring explains the purpose of the view.
    # Approval is role-restricted because not every user should approve portfolio mandates.
    mandate = get_object_or_404(InvestmentMandate, pk=pk)
    # Finds the mandate that the user wants to approve.
    # If it cannot be found, Django returns a 404 page.
    if not request.user.profile.can_approve_mandates:
        # Checks the logged-in user's profile permission.
        # This connects to the accounts app because the user's role is stored in their profile.
        raise PermissionDenied("Only portfolio managers, compliance reviewers or admins can approve mandates.")
        # Stops the request if the user does not have approval permission.
        # This protects the workflow from normal clients or advisers approving mandates incorrectly.
    mandate.status = InvestmentMandate.Status.APPROVED
    # Changes the mandate status to APPROVED using the model's predefined status choices.
    # Using the model constant is safer than typing a random string.
    mandate.approved_by = request.user
    # Records which user approved the mandate.
    mandate.save()
    # Saves the approved status and approver to the database.
    log_action(request.user, "Approved mandate", mandate)
    # Adds an audit log entry so the approval is traceable.
    messages.success(request, "Mandate approved.")
    # Shows a success message to the user.
    return redirect("mandates:detail", pk=mandate.pk)
    # Redirects the user back to the approved mandate detail page.


@login_required
# Only logged-in users can create portfolio holdings.
def holding_create(request):
    # Defines the view used to add a new holding to a mandate.
    if request.method == "POST":
        # Checks whether the holding form has been submitted.
        form = HoldingForm(request.POST)
        # Creates a holding form using the submitted browser data.
        if form.is_valid():
            # Checks that the holding data is valid before saving.
            holding = form.save()
            # Saves the new holding directly to the database.
            # This works because no extra field needs to be added before saving.
            log_action(request.user, "Saved holding", holding)
            # Records that a holding was saved, which supports the audit trail.
            messages.success(request, "Holding saved.")
            # Shows confirmation to the user.
            return redirect("mandates:detail", pk=holding.mandate.pk)
            # Redirects back to the mandate detail page connected to this holding.
            # holding.mandate.pk gets the mandate ID from the relationship.
    else:
        # Runs when the page is opened normally before the form is submitted.
        form = HoldingForm()
        # Creates an empty holding form.
    return render(request, "mandates/holding_form.html", {"form": form})
    # Renders the holding form page and passes the form to the template.

@login_required
# Only logged-in users can delete holdings.
def holding_delete(request, pk):
    # Defines the view used to delete a specific portfolio holding.
    holding = get_object_or_404(PortfolioHolding, pk=pk)
    # Finds the holding by primary key.
    # If it does not exist, Django shows a 404 page.
    mandate_pk = holding.mandate.pk
    # Stores the mandate ID before deleting the holding.
    # This is important because after deletion we still need to redirect back to the mandate page.
    if request.method == "POST":
        # Only deletes the holding if the user confirms through a POST request.
        # This prevents accidental deletion just by visiting a URL.
        log_action(request.user, "Deleted holding", holding, holding.name)
        # Records the delete action before the object is removed from the database.
        # holding.name is used as extra description so the audit log still has useful detail.
        holding.delete()
        # Deletes the holding from the database.
        messages.success(request, "Holding deleted.")
        # Shows a success message after deletion.
        return redirect("mandates:detail", pk=mandate_pk)
        # Redirects back to the related mandate detail page using the saved mandate ID.
    return render(request, "mandates/confirm_delete.html", {"object": holding})
    # If the request is GET, show a confirmation page instead of deleting immediately.
    # The template receives the holding as "object" so it can display what is being deleted.

@login_required
# Only logged-in users can view the list of portfolio review projects.
def project_list(request):
    # Defines the view used to display all portfolio review projects.
    projects = PortfolioReviewProject.objects.select_related("client", "mandate").all()
    # Gets all review projects from the database.
    # select_related loads the related client and mandate efficiently in the same query.
    return render(request, "mandates/project_list.html", {"projects": projects})
    # Renders the project list template and passes all projects into the page.

@login_required
# Only logged-in users can create a portfolio review project.
def project_create(request):
    # Defines the view used to create a new portfolio review project.
    if request.method == "POST":
        # Checks whether the review project form has been submitted.
        form = ReviewProjectForm(request.POST)
        # Creates the form using data submitted by the user.
        if form.is_valid():
            # Checks if the submitted project data is valid.
            project = form.save(commit=False)
            # Creates the project object but does not save it yet.
            # commit=False is used because we need to add created_by first.
            project.created_by = request.user
            # Stores the logged-in user as the creator of the project.
            project.save()
            # Saves the new review project to the PostgreSQL database.
            log_action(request.user, "Created review project", project)
            # Adds an audit log row for the project creation action.
            messages.success(request, "Review project created.")
            # Shows a success message to the user.
            return redirect("mandates:projects")
            # Redirects the user back to the review project list page.
    else:
        # Runs when the user opens the create project page without submitting the form yet.
        form = ReviewProjectForm()
        # Creates an empty review project form.
    return render(request, "mandates/project_form.html", {"form": form})
    # Renders the project form template and passes the form to the HTML page.