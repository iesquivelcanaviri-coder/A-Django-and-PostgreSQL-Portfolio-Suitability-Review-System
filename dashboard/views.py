"""Dashboard views for the portfolio suitability review workflow."""
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render
from clients.models import ClientProfile, RiskAssessment
from mandates.models import InvestmentMandate, PortfolioReviewProject, PortfolioHolding
from messaging.models import Message


def public_home(request):
    """Public landing page explaining the educational purpose of the app."""
    return render(request, "dashboard/public_home.html")


@login_required
def home(request):
    """Authenticated dashboard with portfolio review workflow summaries."""
    context = {
        "client_count": ClientProfile.objects.count(),
        "mandate_count": InvestmentMandate.objects.count(),
        "project_count": PortfolioReviewProject.objects.exclude(status=PortfolioReviewProject.Status.ARCHIVED).count(),
        "unread_count": Message.objects.filter(recipient=request.user, is_read=False, recipient_archived=False).count(),
        "mandates_by_status": InvestmentMandate.objects.values("status").annotate(total=Count("id")).order_by("status"),
        "projects": PortfolioReviewProject.objects.select_related("client", "mandate").all()[:5],
        "risk_assessments": RiskAssessment.objects.select_related("client").all()[:5],
        "holdings": PortfolioHolding.objects.select_related("mandate", "asset_category").all()[:8],
    }
    return render(request, "dashboard/home.html", context)
