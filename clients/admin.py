from django.contrib import admin
# This imports Django's built-in admin module, which gives the project the ready-made admin dashboard at /admin/.
# In the wider Django framework, this connects the app to Django's automatic admin interface.
from .models import ClientProfile, FinancialProfile, RiskAssessment
# This imports the three models from the current app's models.py file. # The dot before models means "look inside this same app folder".
# These models represent the database tables that I want to manage through the Django admin panel.


admin.site.register(ClientProfile)
# This registers the ClientProfile model with the Django admin site.
# It means I can view, add, edit and delete client profile records from /admin/.
# This is useful because ClientProfile stores the client's identity and contact details.
admin.site.register(FinancialProfile)
# This registers the FinancialProfile model with the Django admin site.
# It allows me to manage the client's financial background from the admin panel.
# This connects to the wider portfolio suitability workflow because financial data helps support the suitability review.
admin.site.register(RiskAssessment)
# This registers the RiskAssessment model with the Django admin site.
# It means risk assessment records can be checked and managed through /admin/.
# This is important because the risk assessment is part of the "know the client" and suitability process in the project.