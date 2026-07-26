"""Client and suitability models for the portfolio review workflow."""
from django.conf import settings
# This imports the Django settings file, which lets us refer to the active user model safely using settings.AUTH_USER_MODEL.
from django.db import models
# This imports Django's model system, which is used to create database tables through Python classes.

class ClientProfile(models.Model):
    # This class creates a database table for storing client identity and contact details.
    """Stores identity and contact data for a client or entity."""

    class ClientType(models.TextChoices):
        # TextChoices is a Django helper that lets me create fixed dropdown-style choices for a model field.
        INDIVIDUAL = "INDIVIDUAL", "Individual"
        # This choice stores INDIVIDUAL in the database but displays Individual on forms and admin pages.
        CORPORATE = "CORPORATE", "Corporate"
        # This choice represents a company or business client instead of a personal client.
        FAMILY_OFFICE = "FAMILY_OFFICE", "Family Office"
        # This choice allows the system to record family office clients, which fits a portfolio-management context.
        TRUST = "TRUST", "Trust"
        # This choice allows the system to record trust clients, which may also need portfolio suitability reviews.

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="client_record")
    # This links one client profile to one Django user account, but allows the user link to be empty or removed without deleting the client record.
    full_name = models.CharField(max_length=180)
    # This stores the full name of the client, with a maximum length of 180 characters.
    email = models.EmailField()
    # This stores the client's email address and uses Django's EmailField validation.
    phone = models.CharField(max_length=40, blank=True)
    # This stores the client's phone number, and blank=True means the form can be submitted without this field.
    address = models.CharField(max_length=255, blank=True)
    # This stores the client's address, but it is optional because not every record may need a full address at first.
    tax_residency = models.CharField(max_length=120, blank=True)
    # This stores the client's tax residency, which is useful in a financial suitability or compliance workflow.
    client_type = models.CharField(max_length=30, choices=ClientType.choices, default=ClientType.INDIVIDUAL)
    # This stores the type of client using the fixed choices above, and the default is Individual.
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="clients_created")
    # This links the client record to the user who created it, but keeps the client record if that user is deleted.
    created_at = models.DateTimeField(auto_now_add=True)
    # This automatically records the date and time when the client profile is first created.
    updated_at = models.DateTimeField(auto_now=True)
    # This automatically updates the date and time every time the client profile is saved.

    class Meta:
        # The Meta class is where Django model options are stored, such as ordering or display behaviour.
        ordering = ["full_name"]
        # This orders client profiles alphabetically by full name when they are listed by default.

    def __str__(self):
        # This method controls how the client profile appears as text in the Django admin and query results.
        return self.full_name
        # This returns the client's full name as the readable label for the object.

class FinancialProfile(models.Model):
    # This class creates a database table for storing the client's financial background.
    """Stores financial facts used when assessing portfolio suitability."""

    class LiquidityNeed(models.TextChoices):
        # This creates fixed choices for how much access to cash or liquidity the client needs.
        LOW = "LOW", "Low"
        # This means the client has low liquidity needs and may not need quick access to cash.
        MEDIUM = "MEDIUM", "Medium"
        # This means the client has a moderate liquidity requirement.
        HIGH = "HIGH", "High"
        # This means the client needs higher access to cash or liquid investments.
        MONTHLY = "MONTHLY", "Monthly liquidity required"
        # This means the client needs regular monthly liquidity, which may affect portfolio suitability.

    client = models.OneToOneField(ClientProfile, on_delete=models.CASCADE, related_name="financial_profile")
    # This links one financial profile to one client profile, and deletes the financial profile if the client is deleted.
    net_worth = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    # This stores the client's net worth using DecimalField, which is better than float for financial values.
    existing_investments = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    # This stores the value of the client's existing investments.
    liabilities = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    # This stores debts or obligations, which are important when assessing financial capacity.
    income_band = models.CharField(max_length=80, blank=True)
    # This stores an income range or income description instead of forcing an exact salary amount.
    investment_experience = models.CharField(max_length=120, blank=True)
    # This records the client's investment experience, which helps assess suitability.
    liquidity_need = models.CharField(max_length=30, choices=LiquidityNeed.choices, default=LiquidityNeed.MEDIUM)
    # This stores the client's liquidity need using the fixed LiquidityNeed choices, with Medium as the default.
    time_horizon_years = models.PositiveIntegerField(default=5)
    # This stores the investment time horizon in years, and PositiveIntegerField prevents negative values.
    created_at = models.DateTimeField(auto_now_add=True)
    # This automatically stores when the financial profile was created.
    updated_at = models.DateTimeField(auto_now=True)
    # This automatically stores when the financial profile was last updated.

    def __str__(self):
        # This method controls how the financial profile appears as text.
        return f"Financial profile for {self.client}"
        # This returns a readable label that includes the linked client name.


class RiskAssessment(models.Model):
    # This class creates a database table for storing the client's risk and suitability assessment.
    """Stores suitability assessment information and a simple suitability result."""
    class RiskLevel(models.TextChoices):
        # This creates fixed risk-level choices so the system uses consistent risk labels.
        VERY_LOW = "VERY_LOW", "Very Low"
        # This represents the lowest risk level.
        CONSERVATIVE = "CONSERVATIVE", "Conservative"
        # This represents a cautious risk level.
        BALANCED = "BALANCED", "Balanced"
        # This represents a medium or balanced risk level.
        GROWTH = "GROWTH", "Growth"
        # This represents a higher-risk profile focused on growth.
        AGGRESSIVE = "AGGRESSIVE", "Aggressive"
        # This represents the highest risk level in this educational system.

    class Outcome(models.TextChoices):
        # This creates fixed suitability outcome choices for the result of the assessment.
        SUITABLE = "SUITABLE", "Suitable"
        # This means the risk tolerance and risk capacity are broadly aligned.
        NEEDS_REVIEW = "NEEDS_REVIEW", "Needs Review"
        # This means the assessment needs further review before it can be accepted.
        UNSUITABLE = "UNSUITABLE", "Potentially Unsuitable"
        # This means the difference between tolerance and capacity may be too large.

    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name="risk_assessments")
    # This links each risk assessment to a client, and allows one client to have many assessments over time.
    risk_tolerance = models.CharField(max_length=30, choices=RiskLevel.choices)
    # This stores how much risk the client is willing to take.
    risk_capacity = models.CharField(max_length=30, choices=RiskLevel.choices)
    # This stores how much risk the client can realistically afford to take.
    max_drawdown_percent = models.IntegerField(default=-15)
    # This stores the maximum percentage loss the client may be able to tolerate, using -15 as a default example.
    loss_reaction = models.CharField(max_length=255, blank=True)
    # This records how the client might react to a loss, which helps understand behavioural risk.
    assessment_score = models.PositiveIntegerField(default=0)
    # This stores the calculated suitability score, which is updated automatically in the save method.
    outcome = models.CharField(max_length=30, choices=Outcome.choices, default=Outcome.NEEDS_REVIEW)
    # This stores the final suitability outcome, with Needs Review as the default before calculation.
    review_due_date = models.DateField(null=True, blank=True)
    # This stores when the assessment should be reviewed again, and it is optional.
    assessed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    # This links the assessment to the user who completed it, but keeps the assessment if that user is deleted.
    created_at = models.DateTimeField(auto_now_add=True)
    # This automatically records when the risk assessment was created.
    updated_at = models.DateTimeField(auto_now=True)
    # This automatically records when the risk assessment was last updated.

    class Meta:
        # The Meta class contains model-level options for this table.
        ordering = ["-created_at"]
        # This orders risk assessments by newest first, which is useful when showing recent assessments.

    def save(self, *args, **kwargs):
        # This overrides Django's normal save method so the score and outcome can be calculated before saving.
        """Calculate a simple educational suitability score before saving. This is not investment advice. It is a rules-based classroom example that
        checks whether risk tolerance and risk capacity appear broadly aligned."""
        score_map = {
            # This dictionary converts each risk level into a number so the system can calculate a simple score.
            self.RiskLevel.VERY_LOW: 1,
            # Very Low risk is given the lowest score.
            self.RiskLevel.CONSERVATIVE: 2,
            # Conservative risk is given a low score.
            self.RiskLevel.BALANCED: 3,
            # Balanced risk is given a middle score.
            self.RiskLevel.GROWTH: 4,
            # Growth risk is given a higher score.
            self.RiskLevel.AGGRESSIVE: 5,
            # Aggressive risk is given the highest score.
        }

        tolerance_score = score_map.get(self.risk_tolerance, 3)
        # This gets the numeric score for risk tolerance, using 3 as a safe default if something is missing.
        capacity_score = score_map.get(self.risk_capacity, 3)
        # This gets the numeric score for risk capacity, also using 3 as a default fallback.
        self.assessment_score = tolerance_score + capacity_score
        # This adds tolerance and capacity together to create the total assessment score.
        if abs(tolerance_score - capacity_score) >= 3:
            # This checks whether the gap between risk tolerance and capacity is very large.
            self.outcome = self.Outcome.UNSUITABLE
            # If the gap is very large, the assessment is marked as potentially unsuitable.
        elif abs(tolerance_score - capacity_score) >= 2:
            # This checks whether the gap is moderate and should be reviewed.
            self.outcome = self.Outcome.NEEDS_REVIEW
            # If the gap is moderate, the assessment needs review.
        else:
            # This runs when the risk tolerance and risk capacity are close enough.
            self.outcome = self.Outcome.SUITABLE
            # If the scores are aligned, the outcome is marked as suitable.
        super().save(*args, **kwargs)
        # This calls Django's original save method, which actually writes the record to the database.

    def __str__(self):
        # This method controls how the risk assessment appears as text in the admin and querysets.
        return f"{self.client} - {self.get_outcome_display()}"
        # This returns the client name plus the human-readable suitability outcome.