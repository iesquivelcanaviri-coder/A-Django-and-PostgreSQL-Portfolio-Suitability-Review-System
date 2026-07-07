from django import forms
from .models import ClientProfile, FinancialProfile, RiskAssessment


class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = ["full_name", "email", "phone", "address", "tax_residency", "client_type"]


class FinancialProfileForm(forms.ModelForm):
    class Meta:
        model = FinancialProfile
        fields = ["net_worth", "existing_investments", "liabilities", "income_band", "investment_experience", "liquidity_need", "time_horizon_years"]


class RiskAssessmentForm(forms.ModelForm):
    class Meta:
        model = RiskAssessment
        fields = ["client", "risk_tolerance", "risk_capacity", "max_drawdown_percent", "loss_reaction", "review_due_date"]
        widgets = {"review_due_date": forms.DateInput(attrs={"type": "date"})}
