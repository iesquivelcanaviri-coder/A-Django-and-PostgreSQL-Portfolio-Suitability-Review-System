from django.contrib import admin
from .models import ClientProfile, FinancialProfile, RiskAssessment

admin.site.register(ClientProfile)
admin.site.register(FinancialProfile)
admin.site.register(RiskAssessment)
