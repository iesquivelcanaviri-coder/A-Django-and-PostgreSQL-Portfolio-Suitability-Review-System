"""Dashboard views for the portfolio suitability review workflow."""

from django.contrib.auth.decorators import login_required
# This imports Django's login_required decorator.
# I use this to protect pages so only logged-in users can access the private dashboard.

from django.db.models import Count
# This imports Count from Django's ORM aggregation tools.
# Count lets me group and count database records, for example how many mandates exist for each status.

from django.shortcuts import render
# This imports Django's render shortcut.
# render combines a request, an HTML template, and optional data into a full web page response.

from clients.models import ClientProfile, RiskAssessment
# This imports the client-related models from the clients app.
# ClientProfile stores client records, while RiskAssessment stores suitability/risk assessment results.

from mandates.models import InvestmentMandate, PortfolioReviewProject, PortfolioHolding
# This imports the main portfolio workflow models from the mandates app.
# These models connect the dashboard to mandates, review projects, and portfolio holdings stored in PostgreSQL.

from messaging.models import Message
# This imports the Message model from the messaging app.
# It allows the dashboard to show inbox-related information, such as unread messages for the logged-in user.

from .market_data import get_market_snapshot
# This imports the helper function from dashboard/market_data.py.
# That helper collects the latest market snapshot from Yahoo Finance and sends it to the dashboard.


def public_home(request):
    # This defines the public homepage view.
    # The request parameter represents the HTTP request sent by the browser.

    """Public landing page explaining the educational purpose of the app."""
    # This docstring explains the purpose of this view.
    # This page is public, so it does not require the user to be logged in.

    return render(request, "dashboard/public_home.html")
    # This renders the public_home.html template from the dashboard templates folder.
    # No context dictionary is needed here because the page is mainly static explanatory content.


@login_required
# This decorator protects the home dashboard view.
# If a user is not logged in, Django redirects them to the login page before allowing access.
def home(request):
    # This defines the authenticated dashboard view.
    # This page summarises key records from several apps, so it acts as the main control panel.
    """Authenticated dashboard with portfolio review workflow summaries."""
    # This docstring explains that the dashboard is for logged-in users and shows workflow summaries.
    context = {
        # This dictionary stores all the data that will be sent from the view to the HTML template.
        # In Django, the template can access each key using double curly brackets, such as {{ client_count }}.
        "client_count": ClientProfile.objects.count(),
        # This counts all client profile records in the database.
        # It helps the dashboard show how many clients have been created in the system.
        "mandate_count": InvestmentMandate.objects.count(),
        # This counts all investment mandates in the database.
        # A mandate represents the client's investment rules, objectives, restrictions, and approval status.
        "project_count": PortfolioReviewProject.objects.exclude(status=PortfolioReviewProject.Status.ARCHIVED).count(),
        # This counts portfolio review projects that are not archived.
        # The exclude() query removes archived projects so the dashboard focuses on active or relevant work.
        "unread_count": Message.objects.filter(
            recipient=request.user,
            is_read=False,
            recipient_archived=False
        ).count(),
        # This counts unread messages for the currently logged-in user.
        # request.user is provided by Django authentication and represents the user currently using the app.
        # is_read=False means only unread messages are counted.
        # recipient_archived=False means archived messages are not included in the unread inbox count.
        "mandates_by_status": InvestmentMandate.objects.values("status").annotate(total=Count("id")).order_by("status"),
        # This groups investment mandates by their status and counts how many mandates are in each status.
        # values("status") tells Django to group the results by the status field.
        # annotate(total=Count("id")) creates a new calculated value called total for each status group.
        # order_by("status") sorts the grouped results by status so the output is organised.
        "projects": PortfolioReviewProject.objects.select_related("client", "mandate").all()[:5],
        # This gets the first five portfolio review projects for the dashboard.
        # select_related("client", "mandate") tells Django to fetch linked client and mandate records in the same query.
        # This is more efficient than making separate database queries for each related object.
        # [:5] limits the result to five records so the dashboard stays clean and readable.
        "risk_assessments": RiskAssessment.objects.select_related("client").all()[:5],
        # This gets the first five risk assessments.
        # select_related("client") loads the related client at the same time.
        # This supports the dashboard section showing recent suitability assessment outcomes.
        "holdings": PortfolioHolding.objects.select_related("mandate", "asset_category").all()[:8],
        # This gets the first eight portfolio holdings.
        # select_related("mandate", "asset_category") links each holding to its mandate and asset category efficiently.
        # This helps show how portfolio assets are categorised, such as equities, bonds, cash, or ETFs.
        "market_rows": get_market_snapshot(),
        # This sends the latest Yahoo Finance market data to the dashboard template.
        # The dashboard/home.html file can then loop through this data using {% for row in market_rows %}.
        # This connects the Django view to the external market data helper in dashboard/market_data.py.
    }
    # All the values inside this dictionary can now be used in the dashboard/home.html template.
    return render(request, "dashboard/home.html", context)
    # This renders the private dashboard page.
    # The context dictionary is passed into the template so the HTML page can display live database data.