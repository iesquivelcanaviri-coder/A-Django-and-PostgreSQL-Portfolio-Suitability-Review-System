from django import forms
from .models import InvestmentMandate, PortfolioHolding, PortfolioReviewProject, Stakeholder


class InvestmentMandateForm(forms.ModelForm):
    class Meta:
        model = InvestmentMandate
        fields = ["client", "mandate_name", "objective", "mandate_type", "base_currency", "benchmark", "expected_return_range", "maximum_position_weight", "esg_preference", "product_restriction", "liquidity_requirement", "status"]


class HoldingForm(forms.ModelForm):
    class Meta:
        model = PortfolioHolding
        fields = ["mandate", "asset_category", "name", "ticker", "target_weight", "current_weight", "currency", "risk_notes", "suitability_notes"]


class ReviewProjectForm(forms.ModelForm):
    class Meta:
        model = PortfolioReviewProject
        fields = ["project_name", "description", "client", "mandate", "start_date", "end_date", "status", "priority"]
        widgets = {"start_date": forms.DateInput(attrs={"type": "date"}), "end_date": forms.DateInput(attrs={"type": "date"})}

    def clean(self):
        cleaned = super().clean()
        start = cleaned.get("start_date")
        end = cleaned.get("end_date")
        if start and end and end < start:
            raise forms.ValidationError("End date cannot be before start date.")
        return cleaned


class StakeholderForm(forms.ModelForm):
    class Meta:
        model = Stakeholder
        fields = ["user", "stakeholder_role", "is_active"]
