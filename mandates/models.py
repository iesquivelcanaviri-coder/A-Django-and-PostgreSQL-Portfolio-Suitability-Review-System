"""Mandate, holding, project and audit models."""
from django.conf import settings
# This imports the Django settings file so we can safely refer to the active User model.
from django.db import models
# This imports Django's model tools, which let us create database tables using Python classes.
from clients.models import ClientProfile
# This imports the ClientProfile model from the clients app so mandates and review projects can be linked to clients.

class InvestmentMandate(models.Model):
    # This creates the InvestmentMandate database table using Django's ORM.
    # A mandate represents the agreed investment instructions and restrictions for a client.
    """Stores the agreed portfolio mandate and suitability restrictions."""
    
    class Status(models.TextChoices):
        # TextChoices creates a fixed list of allowed text values for the mandate status.
        # This helps avoid inconsistent status names in the database.
        DRAFT = "DRAFT", "Draft"
        # Draft means the mandate has been started but is not ready for review yet.
        SUBMITTED = "SUBMITTED", "Submitted for Review"
        # Submitted means the adviser has sent the mandate for review or approval.
        MORE_INFO = "MORE_INFO", "More Information Required"
        # More Information Required means the reviewer needs extra details before approving.
        APPROVED = "APPROVED", "Approved"
        # Approved means the mandate has passed the review process.
        REJECTED = "REJECTED", "Rejected"
        # Rejected means the mandate has not been accepted.
        CLOSED = "CLOSED", "Closed"
        # Closed means the mandate is no longer active in the workflow.

    class MandateType(models.TextChoices):
        # This creates another fixed choice list, this time for the type of investment mandate.
        ADVISORY = "ADVISORY", "Advisory"
        # Advisory means the adviser gives recommendations, but the client may still decide.
        DISCRETIONARY = "DISCRETIONARY", "Discretionary"
        # Discretionary means the portfolio manager may make investment decisions within the agreed mandate.

    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name="mandates")
    # This links each mandate to one client.
    # ForeignKey creates a many-to-one relationship: one client can have many mandates.
    # on_delete=models.CASCADE means if the client is deleted, their mandates are also deleted.
    # related_name="mandates" lets us access all mandates from a client using client.mandates.all().
    mandate_name = models.CharField(max_length=180)
    # This stores the name of the mandate as short text.
    # CharField is used for text with a maximum length.
    objective = models.CharField(max_length=255)
    # This stores the main investment objective, such as income, growth, or capital preservation.
    mandate_type = models.CharField(max_length=30, choices=MandateType.choices)
    # This stores whether the mandate is advisory or discretionary.
    # choices=MandateType.choices restricts the value to the options defined above.
    base_currency = models.CharField(max_length=10, default="EUR")
    # This stores the main currency of the mandate.
    # The default is EUR, which means Django uses EUR if no other value is entered.
    benchmark = models.CharField(max_length=80, blank=True)
    # This stores an optional benchmark, such as an index used to compare performance.
    # blank=True means the field can be left empty in forms.
    expected_return_range = models.CharField(max_length=80, blank=True)
    # This stores an educational expected return range as text, for example "3% to 6%".
    # It is text rather than a calculation field because this project is not a trading engine.
    maximum_position_weight = models.DecimalField(max_digits=5, decimal_places=2, default=10)
    # This stores the maximum allowed weight for one holding in the portfolio.
    # DecimalField is better than FloatField for financial values because it avoids floating-point rounding issues.
    # max_digits=5 and decimal_places=2 allow values such as 10.00 or 100.00.
    esg_preference = models.CharField(max_length=120, blank=True)
    # This stores any ESG preference, such as avoiding certain sectors or preferring sustainable assets.
    # blank=True makes it optional.
    product_restriction = models.CharField(max_length=180, blank=True)
    # This stores any product restriction, for example "no derivatives" or "no crypto assets".
    # This supports the suitability and governance purpose of the project.
    liquidity_requirement = models.CharField(max_length=120, blank=True)
    # This stores liquidity needs, such as whether the client needs quick access to money.
    # It is optional because not every mandate may have a specific liquidity note.
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.DRAFT)
    # This stores the current status of the mandate.
    # The default status is Draft when a new mandate is created.
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="mandates_created")
    # This links the mandate to the user who created it.
    # settings.AUTH_USER_MODEL is used instead of importing User directly because it is the recommended Django pattern.
    # on_delete=models.SET_NULL means if the user is deleted, the mandate remains but created_by becomes empty.
    # null=True allows the database field to be empty.
    # related_name="mandates_created" lets us access mandates created by a user using user.mandates_created.all().
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="mandates_approved")
    # This links the mandate to the user who approved it.
    # null=True allows the database to store no approver yet.
    # blank=True allows forms to leave this field empty before approval.
    # This supports the role-based approval workflow in the application.
    created_at = models.DateTimeField(auto_now_add=True)
    # This automatically stores the date and time when the mandate is first created.
    # auto_now_add=True only sets the value once.
    updated_at = models.DateTimeField(auto_now=True)
    # This automatically updates the timestamp every time the mandate is saved.
    # This is useful for showing recent activity and ordering records.

    class Meta:
        # Meta stores extra database and model behaviour for this model.
        ordering = ["-updated_at"]
        # This orders mandates by newest updated first.
        # The minus sign means descending order.

    def __str__(self):
        # This controls how the mandate appears in the Django admin and dropdowns.
        return self.mandate_name
        # This returns the mandate name as the readable label for each mandate object.

class AssetCategory(models.Model):
    # This creates the AssetCategory database table.
    # It is used to group holdings by asset type, such as equities, bonds, ETFs, or cash.
    """Categorises holdings by asset class for portfolio management review."""
    name = models.CharField(max_length=80, unique=True)
    # This stores the category name.
    # unique=True means two categories cannot have the same name.
    description = models.TextField(blank=True)
    # This stores a longer optional explanation of the asset category.
    # TextField is used when the text may be longer than a short CharField.
    risk_level = models.CharField(max_length=40, blank=True)
    # This stores a simple risk label, such as Low, Medium, or High.
    # It supports the educational portfolio review process.

    class Meta:
        # Meta stores additional behaviour for this model.
        ordering = ["name"]
        # This orders categories alphabetically by name.

    def __str__(self):
        # This controls how the asset category appears in admin pages and dropdowns.
        return self.name
        # This returns the category name as the readable label.


class PortfolioHolding(models.Model):
    # This creates the PortfolioHolding database table.
    # A holding is an asset or position linked to a specific investment mandate.
    """Stores an educational portfolio holding linked to a mandate."""
    mandate = models.ForeignKey(InvestmentMandate, on_delete=models.CASCADE, related_name="holdings")
    # This links each holding to one investment mandate.
    # One mandate can have many holdings.
    # If the mandate is deleted, the related holdings are also deleted.
    # related_name="holdings" allows mandate.holdings.all().
    asset_category = models.ForeignKey(AssetCategory, on_delete=models.SET_NULL, null=True, blank=True)
    # This links the holding to an asset category.
    # SET_NULL means if the category is deleted, the holding remains but the category becomes empty.
    # null=True allows the database value to be empty. blank=True allows the form value to be empty.
    name = models.CharField(max_length=150)
    # This stores the holding name, such as Microsoft, Apple, or Government Bond ETF.
    ticker = models.CharField(max_length=20, blank=True)
    # This stores the optional market ticker, such as MSFT or IEF.
    # blank=True allows non-listed assets or educational examples without tickers.
    target_weight = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    # This stores the intended portfolio weight for the holding.
    # For example, 10.00 could mean 10 percent of the portfolio.
    # DecimalField is suitable for financial percentage values.
    current_weight = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    # This stores the current portfolio weight for the holding.
    # This can be compared with target_weight during review.
    currency = models.CharField(max_length=10, default="EUR")
    # This stores the currency of the holding.
    # The default is EUR.
    risk_notes = models.TextField(blank=True)
    # This stores optional notes about risks linked to this holding.
    # TextField is useful for longer explanations.
    suitability_notes = models.TextField(blank=True)
    # This stores optional notes explaining why the holding is or is not suitable for the mandate.
    created_at = models.DateTimeField(auto_now_add=True)
    # This automatically records when the holding was first created.
    updated_at = models.DateTimeField(auto_now=True)
    # This automatically records when the holding was last changed.

    class Meta:
        # Meta stores extra rules for this model.
        unique_together = ["mandate", "ticker"]
        # This prevents the same ticker from being added twice to the same mandate.
        # It is a database-level rule that protects against duplicate holdings.
        ordering = ["-current_weight"]
        # This orders holdings from highest current weight to lowest current weight.
        # This is useful because larger holdings are usually more important in portfolio review.

    def __str__(self):
        # This controls the readable label for the holding.
        return f"{self.name} ({self.current_weight}%)"
        # This returns the holding name and current weight, which makes admin lists easier to read.


class PortfolioReviewProject(models.Model):
    # This creates the PortfolioReviewProject database table.
    # This model directly supports the assignment requirement for project details.
    """Stores project details required by the brief: name, description, dates, stakeholders and status."""
    
    class Status(models.TextChoices):
        # This creates fixed status choices for review projects.
        PLANNED = "PLANNED", "Planned"
        # Planned means the review project has been created but has not started.
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        # In Progress means the review is currently being worked on.
        BLOCKED = "BLOCKED", "Blocked"
        # Blocked means the project cannot continue until an issue is resolved.
        COMPLETE = "COMPLETE", "Complete"
        # Complete means the review project has finished.
        ARCHIVED = "ARCHIVED", "Archived"
        # Archived means the project is kept for recordkeeping but is no longer active.

    project_name = models.CharField(max_length=180)
    # This stores the name of the portfolio review project.
    description = models.TextField()
    # This stores the project description.
    # TextField is used because descriptions can be longer than normal short text.
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE, related_name="review_projects")
    # This links the review project to a client. One client can have many review projects.
    # If the client is deleted, their review projects are also deleted.
    mandate = models.ForeignKey(InvestmentMandate, on_delete=models.SET_NULL, null=True, blank=True, related_name="review_projects")
    # This optionally links the project to an investment mandate.
    # SET_NULL keeps the project even if the mandate is deleted.
    # null=True and blank=True mean a project can exist before a mandate is attached.
    start_date = models.DateField()
    # This stores the planned or actual project start date.
    end_date = models.DateField()
    # This stores the planned or actual project end date.
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.PLANNED)
    # This stores the current status of the review project. The default is Planned.
    priority = models.CharField(max_length=30, default="Medium")
    # This stores a simple priority label, such as Low, Medium, or High.
    # The default value is Medium.
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="projects_created")
    # This links the project to the user who created it.
    # SET_NULL keeps the project record if the creator account is deleted.
    # This is useful for audit and governance evidence.
    stakeholders = models.ManyToManyField(settings.AUTH_USER_MODEL, through="Stakeholder", related_name="portfolio_projects")
    # This links many users to many projects.
    # through="Stakeholder" means Django uses the custom Stakeholder model as the joining table.
    # This is useful because the Stakeholder model stores extra information, such as stakeholder_role and is_active.
    created_at = models.DateTimeField(auto_now_add=True)
    # This automatically records when the project was created.
    updated_at = models.DateTimeField(auto_now=True)
    # This automatically records when the project was last updated.

    class Meta:
        # Meta stores additional model settings.
        ordering = ["-start_date"]
        # This orders projects by newest start date first.

    def __str__(self):
        # This controls how the project appears in Django admin and dropdowns.
        return self.project_name
        # This returns the project name as the readable label.

class Stakeholder(models.Model):
    # This creates the Stakeholder database table.
    # It works as a custom joining table between users and portfolio review projects.
    """Links users to projects with a clear stakeholder role."""
    project = models.ForeignKey(PortfolioReviewProject, on_delete=models.CASCADE)
    # This links the stakeholder record to one portfolio review project.
    # If the project is deleted, the stakeholder link is also deleted.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # This links the stakeholder record to one Django user.
    # If the user is deleted, the stakeholder link is also deleted.
    stakeholder_role = models.CharField(max_length=80)
    # This stores the role of the user within the project.
    # Examples could include Adviser, Reviewer, Client, or Portfolio Manager.
    date_added = models.DateTimeField(auto_now_add=True)
    # This automatically records when the user was added as a stakeholder.
    is_active = models.BooleanField(default=True)
    # This shows whether the stakeholder is currently active on the project.
    # BooleanField stores True or False values.

    class Meta:
        # Meta stores database-level rules for this model.
        unique_together = ["project", "user"]
        # This prevents the same user from being added twice to the same project.

    def __str__(self):
        # This controls how the stakeholder record appears in admin and dropdowns.
        return f"{self.user} - {self.stakeholder_role}"
        # This returns the user and their project role, making the record easier to identify.


class AuditLog(models.Model):
    # This creates the AuditLog database table.
    # It records important actions for governance and evidence.
    """Simple governance log for important portfolio workflow actions."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    # This links the log entry to the user who performed the action.
    # SET_NULL keeps the log even if the user account is deleted.
    action = models.CharField(max_length=120)
    # This stores the action name, such as Created, Updated, Approved, Rejected, or Archived.
    model_name = models.CharField(max_length=80)
    # This stores the model affected by the action, such as InvestmentMandate or PortfolioReviewProject.
    object_id = models.PositiveIntegerField(null=True, blank=True)
    # This stores the ID of the object affected by the action.
    # PositiveIntegerField is used because database IDs are usually positive numbers.
    # null=True and blank=True allow the field to be empty if no specific object is linked.
    description = models.TextField(blank=True)
    # This stores optional extra detail about what happened. This helps explain the action later.
    timestamp = models.DateTimeField(auto_now_add=True)
    # This automatically records when the audit log entry was created.

    class Meta:
        # Meta stores extra model behaviour.
        ordering = ["-timestamp"]
        # This orders audit logs by newest first.
        # This is useful because recent governance activity is usually reviewed first.

    def __str__(self):
        # This controls how the audit log appears in admin pages and dropdowns.
        return f"{self.action} - {self.model_name}"
        # This returns a short readable label showing the action and affected model.