"""Mandate, holding, project and audit models."""
from django.conf import settings
from django.db import models
from clients.models import ClientProfile


class InvestmentMandate(models.Model):
    """Stores the agreed portfolio mandate and suitability restrictions."""

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        SUBMITTED = "SUBMITTED", "Submitted for Review"
        MORE_INFO = "MORE_INFO", "More Information Required"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"
        CLOSED = "CLOSED", "Closed"

    class MandateType(models.TextChoices):
        ADVISORY = "ADVISORY", "Advisory"
        DISCRETIONARY = "DISCRETIONARY", "Discretionary"

    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name="mandates")
    mandate_name = models.CharField(max_length=180)
    objective = models.CharField(max_length=255)
    mandate_type = models.CharField(max_length=30, choices=MandateType.choices)
    base_currency = models.CharField(max_length=10, default="EUR")
    benchmark = models.CharField(max_length=80, blank=True)
    expected_return_range = models.CharField(max_length=80, blank=True)
    maximum_position_weight = models.DecimalField(max_digits=5, decimal_places=2, default=10)
    esg_preference = models.CharField(max_length=120, blank=True)
    product_restriction = models.CharField(max_length=180, blank=True)
    liquidity_requirement = models.CharField(max_length=120, blank=True)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.DRAFT)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="mandates_created")
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="mandates_approved")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.mandate_name


class AssetCategory(models.Model):
    """Categorises holdings by asset class for portfolio management review."""
    name = models.CharField(max_length=80, unique=True)
    description = models.TextField(blank=True)
    risk_level = models.CharField(max_length=40, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class PortfolioHolding(models.Model):
    """Stores an educational portfolio holding linked to a mandate."""
    mandate = models.ForeignKey(InvestmentMandate, on_delete=models.CASCADE, related_name="holdings")
    asset_category = models.ForeignKey(AssetCategory, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=150)
    ticker = models.CharField(max_length=20, blank=True)
    target_weight = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    current_weight = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    currency = models.CharField(max_length=10, default="EUR")
    risk_notes = models.TextField(blank=True)
    suitability_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["mandate", "ticker"]
        ordering = ["-current_weight"]

    def __str__(self):
        return f"{self.name} ({self.current_weight}%)"


class PortfolioReviewProject(models.Model):
    """Stores project details required by the brief: name, description, dates, stakeholders and status."""

    class Status(models.TextChoices):
        PLANNED = "PLANNED", "Planned"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        BLOCKED = "BLOCKED", "Blocked"
        COMPLETE = "COMPLETE", "Complete"
        ARCHIVED = "ARCHIVED", "Archived"

    project_name = models.CharField(max_length=180)
    description = models.TextField()
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name="review_projects")
    mandate = models.ForeignKey(InvestmentMandate, on_delete=models.SET_NULL, null=True, blank=True, related_name="review_projects")
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.PLANNED)
    priority = models.CharField(max_length=30, default="Medium")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="projects_created")
    stakeholders = models.ManyToManyField(settings.AUTH_USER_MODEL, through="Stakeholder", related_name="portfolio_projects")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return self.project_name


class Stakeholder(models.Model):
    """Links users to projects with a clear stakeholder role."""
    project = models.ForeignKey(PortfolioReviewProject, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stakeholder_role = models.CharField(max_length=80)
    date_added = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ["project", "user"]

    def __str__(self):
        return f"{self.user} - {self.stakeholder_role}"


class AuditLog(models.Model):
    """Simple governance log for important portfolio workflow actions."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=120)
    model_name = models.CharField(max_length=80)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.action} - {self.model_name}"
