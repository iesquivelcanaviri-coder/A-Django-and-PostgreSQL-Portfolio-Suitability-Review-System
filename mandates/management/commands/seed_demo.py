"""Seed a small educational dataset for assessment screenshots and testing."""
from django.contrib.auth.models import User
# This imports Django's built-in User model, which stores usernames, emails, passwords and authentication details.
from django.core.management.base import BaseCommand
# This imports BaseCommand, which is needed to create a custom Django management command that can run from the terminal.
from clients.models import ClientProfile, FinancialProfile, RiskAssessment
# This imports the client-related models so the command can create demo client, financial and risk assessment records.
from mandates.models import AssetCategory, InvestmentMandate, PortfolioHolding, PortfolioReviewProject
# This imports the mandate-related models, which are the main portfolio suitability workflow models in the project.
from messaging.models import Message
# This imports the Message model so the command can create an example inbox message between users.
from datetime import date, timedelta
# This imports date and timedelta so the command can set today's date and future dates such as review deadlines.

class Command(BaseCommand):
    # Every Django management command needs a Command class that inherits from BaseCommand.
    help = "Create demo users, client records, mandates, holdings, projects and messages."
    # This help text appears if someone runs the command with --help, so it explains what this seed command does.

    def handle(self, *args, **options):
        # The handle method is the main method Django runs when this command is executed in the terminal.
        adviser, _ = User.objects.get_or_create(username="adviser", defaults={"email": "adviser@example.com", "first_name": "Demo", "last_name": "Adviser"})
        # This creates a demo adviser user if it does not already exist, or gets the existing one if it is already in the database.
        adviser.set_password("ChangeMe123!")
        # This sets the adviser's password using Django's password hashing system instead of saving the password as plain text.
        adviser.save()
        # This saves the adviser user to the database after setting the password.
        adviser.profile.role = "ADVISER"
        # This updates the linked UserProfile role so the user behaves as an Adviser in the project workflow.
        adviser.profile.save()
        # This saves the updated profile role to the database.
        manager, _ = User.objects.get_or_create(username="manager", defaults={"email": "manager@example.com", "first_name": "Portfolio", "last_name": "Manager"})
        # This creates or retrieves a second demo user called manager, who represents the portfolio manager role.
        manager.set_password("ChangeMe123!")
        # This sets the manager's password securely using Django's built-in password handling.
        manager.save()
        # This saves the manager user after the password has been set.
        manager.profile.role = "PORTFOLIO_MANAGER"
        # This gives the manager user the Portfolio Manager role, which is important for role-based approval logic.
        manager.profile.save()
        # This saves the manager's updated profile role to the database.
        client = ClientProfile.objects.create(
            # This creates a new client profile record and stores it in the PostgreSQL database.
            full_name="Emma Keller",
            # This stores the client's full name as demo client identity data.
            email="emma.keller@example.com",
            # This stores the client's email address for contact information.
            phone="+353 1 000 0000",
            # This stores the client's phone number as part of the client profile.
            tax_residency="Ireland",
            # This stores the client's tax residency, which is realistic information in a suitability review process.
            client_type="INDIVIDUAL",
            # This marks the client as an individual rather than another type of client.
            created_by=adviser,
            # This links the client profile to the adviser user who created it, showing database relationships through foreign keys.
        )

        FinancialProfile.objects.create(client=client, net_worth=850000, existing_investments=300000, liabilities=120000, income_band="100k-150k", investment_experience="Intermediate", liquidity_need="MEDIUM", time_horizon_years=10)
        # This creates the client's financial profile, which supports the know-your-client and suitability part of the portfolio workflow.
        RiskAssessment.objects.create(client=client, risk_tolerance="BALANCED", risk_capacity="GROWTH", max_drawdown_percent=-15, loss_reaction="Can tolerate moderate losses with advice", review_due_date=date.today() + timedelta(days=365), assessed_by=adviser)
        # This creates a risk assessment linked to the client, including tolerance, capacity, drawdown comfort and a future review date.
        equity, _ = AssetCategory.objects.get_or_create(name="Global Equities", defaults={"risk_level": "Medium-High", "description": "Diversified global equity exposure"})
        # This creates or retrieves an asset category for global equities, which is used to categorise portfolio holdings.
        bonds, _ = AssetCategory.objects.get_or_create(name="Government Bonds", defaults={"risk_level": "Low-Medium", "description": "Defensive bond allocation"})
        # This creates or retrieves an asset category for government bonds, which supports categorised portfolio data.
        mandate = InvestmentMandate.objects.create(client=client, mandate_name="Emma Keller Balanced Growth Mandate", objective="Balanced long-term growth with liquidity discipline", mandate_type="ADVISORY", base_currency="EUR", benchmark="60/40 global benchmark", expected_return_range="5-7%", maximum_position_weight=10, esg_preference="ESG considered", product_restriction="UCITS preferred", liquidity_requirement="Medium", status="SUBMITTED", created_by=adviser)
        # This creates an investment mandate linked to the client, showing the main portfolio suitability instruction and approval workflow.
        PortfolioHolding.objects.create(mandate=mandate, asset_category=equity, name="Global Equity ETF", ticker="ACWI", target_weight=60, current_weight=55, currency="USD", suitability_notes="Supports long-term growth objective")
        # This creates a portfolio holding linked to the mandate and categorised as global equities.
        PortfolioHolding.objects.create(mandate=mandate, asset_category=bonds, name="Treasury Bond ETF", ticker="IEF", target_weight=40, current_weight=35, currency="USD", suitability_notes="Defensive allocation for volatility control")
        # This creates a second portfolio holding linked to the same mandate and categorised as government bonds.
        project = PortfolioReviewProject.objects.create(project_name="Annual Suitability Review 2026", description="Review client risk profile, mandate restrictions and portfolio allocation.", client=client, mandate=mandate, start_date=date.today(), end_date=date.today() + timedelta(days=30), status="IN_PROGRESS", priority="High", created_by=adviser)
        # This creates a portfolio review project, which is useful evidence for the assignment requirement about storing project details.
        Message.objects.create(sender=adviser, recipient=manager, subject="Please review Emma Keller mandate", body="The suitability assessment and proposed mandate are ready for review.", related_project=project)
        # This creates an internal message from the adviser to the portfolio manager and links it to the review project.
        self.stdout.write(self.style.SUCCESS("Demo data created. Login as adviser or manager with password ChangeMe123!"))
        # This prints a success message in the terminal so the user knows the seed command worked.