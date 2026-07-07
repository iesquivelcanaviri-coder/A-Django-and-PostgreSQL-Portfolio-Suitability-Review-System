"""Views for mandate, holdings and portfolio review project CRUD."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from .forms import HoldingForm, InvestmentMandateForm, ReviewProjectForm
from .models import AuditLog, InvestmentMandate, PortfolioHolding, PortfolioReviewProject


def log_action(user, action, instance, description=""):
    """Save a small audit log row for important workflow actions."""
    AuditLog.objects.create(user=user, action=action, model_name=instance.__class__.__name__, object_id=instance.pk, description=description)


@login_required
def mandate_list(request):
    mandates = InvestmentMandate.objects.select_related("client", "approved_by").all()
    return render(request, "mandates/mandate_list.html", {"mandates": mandates})


@login_required
def mandate_create(request):
    if request.method == "POST":
        form = InvestmentMandateForm(request.POST)
        if form.is_valid():
            mandate = form.save(commit=False)
            mandate.created_by = request.user
            mandate.save()
            log_action(request.user, "Created mandate", mandate)
            messages.success(request, "Investment mandate created.")
            return redirect("mandates:detail", pk=mandate.pk)
    else:
        form = InvestmentMandateForm()
    return render(request, "mandates/mandate_form.html", {"form": form, "title": "Create Investment Mandate"})


@login_required
def mandate_detail(request, pk):
    mandate = get_object_or_404(InvestmentMandate, pk=pk)
    return render(request, "mandates/mandate_detail.html", {"mandate": mandate})


@login_required
def mandate_update(request, pk):
    mandate = get_object_or_404(InvestmentMandate, pk=pk)
    if request.method == "POST":
        form = InvestmentMandateForm(request.POST, instance=mandate)
        if form.is_valid():
            mandate = form.save()
            log_action(request.user, "Updated mandate", mandate)
            messages.success(request, "Investment mandate updated.")
            return redirect("mandates:detail", pk=mandate.pk)
    else:
        form = InvestmentMandateForm(instance=mandate)
    return render(request, "mandates/mandate_form.html", {"form": form, "title": "Update Investment Mandate"})


@login_required
def mandate_approve(request, pk):
    """Approve a mandate only when the user has a portfolio/compliance role."""
    mandate = get_object_or_404(InvestmentMandate, pk=pk)
    if not request.user.profile.can_approve_mandates:
        raise PermissionDenied("Only portfolio managers, compliance reviewers or admins can approve mandates.")
    mandate.status = InvestmentMandate.Status.APPROVED
    mandate.approved_by = request.user
    mandate.save()
    log_action(request.user, "Approved mandate", mandate)
    messages.success(request, "Mandate approved.")
    return redirect("mandates:detail", pk=mandate.pk)


@login_required
def holding_create(request):
    if request.method == "POST":
        form = HoldingForm(request.POST)
        if form.is_valid():
            holding = form.save()
            log_action(request.user, "Saved holding", holding)
            messages.success(request, "Holding saved.")
            return redirect("mandates:detail", pk=holding.mandate.pk)
    else:
        form = HoldingForm()
    return render(request, "mandates/holding_form.html", {"form": form})


@login_required
def holding_delete(request, pk):
    holding = get_object_or_404(PortfolioHolding, pk=pk)
    mandate_pk = holding.mandate.pk
    if request.method == "POST":
        log_action(request.user, "Deleted holding", holding, holding.name)
        holding.delete()
        messages.success(request, "Holding deleted.")
        return redirect("mandates:detail", pk=mandate_pk)
    return render(request, "mandates/confirm_delete.html", {"object": holding})


@login_required
def project_list(request):
    projects = PortfolioReviewProject.objects.select_related("client", "mandate").all()
    return render(request, "mandates/project_list.html", {"projects": projects})


@login_required
def project_create(request):
    if request.method == "POST":
        form = ReviewProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()
            log_action(request.user, "Created review project", project)
            messages.success(request, "Review project created.")
            return redirect("mandates:projects")
    else:
        form = ReviewProjectForm()
    return render(request, "mandates/project_form.html", {"form": form})
