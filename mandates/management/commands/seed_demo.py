"""Seed a small educational dataset for assessment screenshots and testing."""
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from clients.models import ClientProfile, FinancialProfile, RiskAssessment
from mandates.models import AssetCategory, InvestmentMandate, PortfolioHolding, PortfolioReviewProject
from messaging.models import Message
from datetime import date, timedelta


class Command(BaseCommand):
    help = "Create demo users, client records, mandates, holdings, projects and messages."

    def handle(self, *args, **options):
        adviser, _ = User.objects.get_or_create(username="adviser", defaults={"email": "adviser@example.com", "first_name": "Demo", "last_name": "Adviser"})
        adviser.set_password("ChangeMe123!")
        adviser.save()
        adviser.profile.role = "ADVISER"
        adviser.profile.save()

        manager, _ = User.objects.get_or_create(username="manager", defaults={"email": "manager@example.com", "first_name": "Portfolio", "last_name": "Manager"})
        manager.set_password("ChangeMe123!")
        manager.save()
        manager.profile.role = "PORTFOLIO_MANAGER"
        manager.profile.save()

        client = ClientProfile.objects.create(
            full_name="Emma Keller",
            email="emma.keller@example.com",
            phone="+353 1 000 0000",
            tax_residency="Ireland",
            client_type="INDIVIDUAL",
            created_by=adviser,
        )
        FinancialProfile.objects.create(client=client, net_worth=850000, existing_investments=300000, liabilities=120000, income_band="100k-150k", investment_experience="Intermediate", liquidity_need="MEDIUM", time_horizon_years=10)
        RiskAssessment.objects.create(client=client, risk_tolerance="BALANCED", risk_capacity="GROWTH", max_drawdown_percent=-15, loss_reaction="Can tolerate moderate losses with advice", review_due_date=date.today() + timedelta(days=365), assessed_by=adviser)

        equity, _ = AssetCategory.objects.get_or_create(name="Global Equities", defaults={"risk_level": "Medium-High", "description": "Diversified global equity exposure"})
        bonds, _ = AssetCategory.objects.get_or_create(name="Government Bonds", defaults={"risk_level": "Low-Medium", "description": "Defensive bond allocation"})

        mandate = InvestmentMandate.objects.create(client=client, mandate_name="Emma Keller Balanced Growth Mandate", objective="Balanced long-term growth with liquidity discipline", mandate_type="ADVISORY", base_currency="EUR", benchmark="60/40 global benchmark", expected_return_range="5-7%", maximum_position_weight=10, esg_preference="ESG considered", product_restriction="UCITS preferred", liquidity_requirement="Medium", status="SUBMITTED", created_by=adviser)
        PortfolioHolding.objects.create(mandate=mandate, asset_category=equity, name="Global Equity ETF", ticker="ACWI", target_weight=60, current_weight=55, currency="USD", suitability_notes="Supports long-term growth objective")
        PortfolioHolding.objects.create(mandate=mandate, asset_category=bonds, name="Treasury Bond ETF", ticker="IEF", target_weight=40, current_weight=35, currency="USD", suitability_notes="Defensive allocation for volatility control")
        project = PortfolioReviewProject.objects.create(project_name="Annual Suitability Review 2026", description="Review client risk profile, mandate restrictions and portfolio allocation.", client=client, mandate=mandate, start_date=date.today(), end_date=date.today() + timedelta(days=30), status="IN_PROGRESS", priority="High", created_by=adviser)
        Message.objects.create(sender=adviser, recipient=manager, subject="Please review Emma Keller mandate", body="The suitability assessment and proposed mandate are ready for review.", related_project=project)
        self.stdout.write(self.style.SUCCESS("Demo data created. Login as adviser or manager with password ChangeMe123!"))
