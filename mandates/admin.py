from django.contrib import admin
from .models import AssetCategory, AuditLog, InvestmentMandate, PortfolioHolding, PortfolioReviewProject, Stakeholder

admin.site.register(AssetCategory)
admin.site.register(AuditLog)
admin.site.register(InvestmentMandate)
admin.site.register(PortfolioHolding)
admin.site.register(PortfolioReviewProject)
admin.site.register(Stakeholder)
