from django import forms
# Imports Django's forms module, which gives us tools like ModelForm, DateInput and ValidationError for building forms connected to Django models.
from .models import InvestmentMandate, PortfolioHolding, PortfolioReviewProject, Stakeholder
# Imports the models from the current mandates app so each form can be linked directly to a database table through Django's ORM.

class InvestmentMandateForm(forms.ModelForm):
    # Creates a form class for the InvestmentMandate model, using Django's ModelForm so the form fields are generated from the model automatically.
    class Meta:
        # The Meta class tells Django which model this form belongs to and which model fields should appear on the form.
        model = InvestmentMandate
        # Connects this form to the InvestmentMandate model, meaning submitted form data can be saved into the investment mandate database table.
        fields = ["client", "mandate_name", "objective", "mandate_type", "base_currency", "benchmark", "expected_return_range", "maximum_position_weight", "esg_preference", "product_restriction", "liquidity_requirement", "status"]
        # Lists the exact model fields that should appear in the form, so the user can enter mandate details such as client, objective, benchmark, ESG preference and status.

class HoldingForm(forms.ModelForm):
    # Creates a form class for portfolio holdings, so users can add or edit individual assets linked to an investment mandate.
    class Meta:
        # The Meta class defines the model connection and selected fields for this holding form.
        model = PortfolioHolding
        # Links this form to the PortfolioHolding model, meaning each submitted holding can be stored in the portfolio holding database table.
        fields = ["mandate", "asset_category", "name", "ticker", "target_weight", "current_weight", "currency", "risk_notes", "suitability_notes"]
        # These fields allow the user to record what the holding is, how it is categorised, its target/current allocation and any risk or suitability notes.

class ReviewProjectForm(forms.ModelForm):
    # Creates a form for portfolio review projects, which helps manage review work such as project dates, priority and status.
    class Meta:
        # The Meta class gives Django the instructions for generating this form from the PortfolioReviewProject model.
        model = PortfolioReviewProject
        # Connects this form to the PortfolioReviewProject model, so project review details can be saved into the PostgreSQL database.
        fields = ["project_name", "description", "client", "mandate", "start_date", "end_date", "status", "priority"]
        # These fields match the assignment requirement to store project details such as name, description, dates, status and related stakeholders or workflow information.
        widgets = {"start_date": forms.DateInput(attrs={"type": "date"}), "end_date": forms.DateInput(attrs={"type": "date"})}
        # Changes the start_date and end_date fields into browser date pickers, making the form easier to use in the HTML template.

    def clean(self):
        # Defines custom form validation that runs after Django has collected and checked the individual field values.
        cleaned = super().clean()
        # Calls Django's normal ModelForm clean method first, so the default validation still happens before my custom validation.
        start = cleaned.get("start_date")
        # Gets the submitted start date from the cleaned data dictionary after Django has processed the form input.
        end = cleaned.get("end_date")
        # Gets the submitted end date from the cleaned data dictionary so it can be compared with the start date.
        if start and end and end < start:
            # Checks that both dates exist and then makes sure the end date is not earlier than the start date.
            raise forms.ValidationError("End date cannot be before start date.")
            # Raises a form-level validation error, which means the form will not save and the user will see this message on the page.
        return cleaned
        # Returns the cleaned data back to Django if there are no validation errors, allowing the form to continue saving normally.

class StakeholderForm(forms.ModelForm):
    # Creates a form for adding or updating stakeholders linked to a portfolio review project.
    class Meta:
        # The Meta class tells Django which model this stakeholder form is based on and which fields should be displayed.
        model = Stakeholder
        # Links this form to the Stakeholder model, so stakeholder records are saved into the database.
        fields = ["user", "stakeholder_role", "is_active"]
        # Allows the user to choose the stakeholder user, define their role in the project and mark whether the stakeholder is active.