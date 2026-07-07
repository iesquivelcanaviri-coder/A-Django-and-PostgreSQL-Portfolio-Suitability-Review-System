"""Views for client profile, financial profile and risk assessment CRUD."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ClientProfileForm, FinancialProfileForm, RiskAssessmentForm
from .models import ClientProfile, FinancialProfile, RiskAssessment


@login_required
def client_list(request):
    """Show all client records visible to logged-in users for the prototype."""
    clients = ClientProfile.objects.select_related("financial_profile").all()
    return render(request, "clients/client_list.html", {"clients": clients})


@login_required
def client_create(request):
    """Create a new client profile record."""
    if request.method == "POST":
        form = ClientProfileForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.created_by = request.user
            client.save()
            messages.success(request, "Client profile created.")
            return redirect("clients:detail", pk=client.pk)
    else:
        form = ClientProfileForm()
    return render(request, "clients/client_form.html", {"form": form, "title": "Create Client Profile"})


@login_required
def client_detail(request, pk):
    """Read one client profile with financial, risk and mandate context."""
    client = get_object_or_404(ClientProfile, pk=pk)
    return render(request, "clients/client_detail.html", {"client": client})


@login_required
def client_update(request, pk):
    """Update an existing client profile."""
    client = get_object_or_404(ClientProfile, pk=pk)
    if request.method == "POST":
        form = ClientProfileForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, "Client profile updated.")
            return redirect("clients:detail", pk=client.pk)
    else:
        form = ClientProfileForm(instance=client)
    return render(request, "clients/client_form.html", {"form": form, "title": "Update Client Profile"})


@login_required
def financial_profile_edit(request, client_pk):
    """Create or update the financial profile linked to a client."""
    client = get_object_or_404(ClientProfile, pk=client_pk)
    profile, _created = FinancialProfile.objects.get_or_create(client=client)
    if request.method == "POST":
        form = FinancialProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Financial profile saved.")
            return redirect("clients:detail", pk=client.pk)
    else:
        form = FinancialProfileForm(instance=profile)
    return render(request, "clients/client_form.html", {"form": form, "title": "Financial Profile"})


@login_required
def risk_assessment_create(request):
    """Create a risk assessment and automatically calculate the outcome."""
    if request.method == "POST":
        form = RiskAssessmentForm(request.POST)
        if form.is_valid():
            assessment = form.save(commit=False)
            assessment.assessed_by = request.user
            assessment.save()
            messages.success(request, f"Risk assessment saved: {assessment.get_outcome_display()}.")
            return redirect("clients:detail", pk=assessment.client.pk)
    else:
        form = RiskAssessmentForm()
    return render(request, "clients/risk_form.html", {"form": form})
