"""Client and suitability models for the portfolio review workflow."""
from django.conf import settings
from django.db import models


class ClientProfile(models.Model):
    """Stores identity and contact data for a client or entity."""

    class ClientType(models.TextChoices):
        INDIVIDUAL = "INDIVIDUAL", "Individual"
        CORPORATE = "CORPORATE", "Corporate"
        FAMILY_OFFICE = "FAMILY_OFFICE", "Family Office"
        TRUST = "TRUST", "Trust"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="client_record")
    full_name = models.CharField(max_length=180)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    address = models.CharField(max_length=255, blank=True)
    tax_residency = models.CharField(max_length=120, blank=True)
    client_type = models.CharField(max_length=30, choices=ClientType.choices, default=ClientType.INDIVIDUAL)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="clients_created")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["full_name"]

    def __str__(self):
        return self.full_name


class FinancialProfile(models.Model):
    """Stores financial facts used when assessing portfolio suitability."""

    class LiquidityNeed(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"
        MONTHLY = "MONTHLY", "Monthly liquidity required"

    client = models.OneToOneField(ClientProfile, on_delete=models.CASCADE, related_name="financial_profile")
    net_worth = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    existing_investments = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    liabilities = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    income_band = models.CharField(max_length=80, blank=True)
    investment_experience = models.CharField(max_length=120, blank=True)
    liquidity_need = models.CharField(max_length=30, choices=LiquidityNeed.choices, default=LiquidityNeed.MEDIUM)
    time_horizon_years = models.PositiveIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Financial profile for {self.client}"


class RiskAssessment(models.Model):
    """Stores suitability assessment information and a simple suitability result."""

    class RiskLevel(models.TextChoices):
        VERY_LOW = "VERY_LOW", "Very Low"
        CONSERVATIVE = "CONSERVATIVE", "Conservative"
        BALANCED = "BALANCED", "Balanced"
        GROWTH = "GROWTH", "Growth"
        AGGRESSIVE = "AGGRESSIVE", "Aggressive"

    class Outcome(models.TextChoices):
        SUITABLE = "SUITABLE", "Suitable"
        NEEDS_REVIEW = "NEEDS_REVIEW", "Needs Review"
        UNSUITABLE = "UNSUITABLE", "Potentially Unsuitable"

    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name="risk_assessments")
    risk_tolerance = models.CharField(max_length=30, choices=RiskLevel.choices)
    risk_capacity = models.CharField(max_length=30, choices=RiskLevel.choices)
    max_drawdown_percent = models.IntegerField(default=-15)
    loss_reaction = models.CharField(max_length=255, blank=True)
    assessment_score = models.PositiveIntegerField(default=0)
    outcome = models.CharField(max_length=30, choices=Outcome.choices, default=Outcome.NEEDS_REVIEW)
    review_due_date = models.DateField(null=True, blank=True)
    assessed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        """Calculate a simple educational suitability score before saving.

        This is not investment advice. It is a rules-based classroom example that
        checks whether risk tolerance and risk capacity appear broadly aligned.
        """
        score_map = {
            self.RiskLevel.VERY_LOW: 1,
            self.RiskLevel.CONSERVATIVE: 2,
            self.RiskLevel.BALANCED: 3,
            self.RiskLevel.GROWTH: 4,
            self.RiskLevel.AGGRESSIVE: 5,
        }
        tolerance_score = score_map.get(self.risk_tolerance, 3)
        capacity_score = score_map.get(self.risk_capacity, 3)
        self.assessment_score = tolerance_score + capacity_score
        if abs(tolerance_score - capacity_score) >= 3:
            self.outcome = self.Outcome.UNSUITABLE
        elif abs(tolerance_score - capacity_score) >= 2:
            self.outcome = self.Outcome.NEEDS_REVIEW
        else:
            self.outcome = self.Outcome.SUITABLE
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.client} - {self.get_outcome_display()}"
