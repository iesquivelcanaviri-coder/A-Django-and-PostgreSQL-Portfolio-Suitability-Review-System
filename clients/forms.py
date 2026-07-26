from django import forms
# I import Django's forms module because this file is responsible for creating form classes that Django can use in templates and views.
from .models import ClientProfile, FinancialProfile, RiskAssessment
# I import the three models from the current app's models.py file because each ModelForm below is directly connected to one database model.


class ClientProfileForm(forms.ModelForm):
    # This form is based on the ClientProfile model, so Django can automatically build form fields from the model fields.
    class Meta:
        # The Meta class tells Django which model this form belongs to and which fields should appear on the web form.
        model = ClientProfile
        # This connects the form to the ClientProfile database table, meaning saved form data will create or update a client profile record.
        fields = ["full_name", "email", "phone", "address", "tax_residency", "client_type"]
        # These are the exact ClientProfile fields that will be shown in the form, so the user can enter client identity and contact details.


class FinancialProfileForm(forms.ModelForm):
    # This form is used to collect the client's financial background, which supports the suitability review process.
    class Meta:
        # The Meta class is used again because this is also a ModelForm connected to a database model.
        model = FinancialProfile
        # This links the form to the FinancialProfile model, so Django knows which database table should receive the submitted financial data.
        fields = ["net_worth", "existing_investments", "liabilities", "income_band", "investment_experience", "liquidity_need", "time_horizon_years"]
        # These fields allow the app to collect important financial suitability information such as wealth, liabilities, experience and investment time horizon.


class RiskAssessmentForm(forms.ModelForm):
    # This form collects the client's risk assessment information, which is important for deciding if a mandate is suitable.
    class Meta:
        # The Meta class defines the model connection, form fields and any custom widgets for this risk assessment form.
        model = RiskAssessment
        # This connects the form to the RiskAssessment model, so the risk answers can be stored in the PostgreSQL database.
        fields = ["client", "risk_tolerance", "risk_capacity", "max_drawdown_percent", "loss_reaction", "review_due_date"]
        # These are the fields shown on the form, including the linked client, risk level, loss reaction and next review date.
        widgets = {"review_due_date": forms.DateInput(attrs={"type": "date"})}
        # This changes the review_due_date field into a browser date picker, which makes the form easier to use and reduces date-format mistakes.