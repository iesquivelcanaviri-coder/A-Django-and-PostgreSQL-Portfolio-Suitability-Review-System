from django.contrib import admin
# This imports Django's built-in admin module.
# The admin module gives the project the ready-made Django admin dashboard at /admin/.
# In the wider Django framework, this is useful because it lets me manage database records without building custom pages first.
from .models import ClientProfile, FinancialProfile, RiskAssessment
# This imports the three models from the current app's models.py file.
# The dot before models means "look inside this same clients app folder".
# Each model represents a database table that Django created through migrations.
# By importing them here, I can connect these database tables to the Django admin panel.


admin.site.register(ClientProfile)
# This registers the ClientProfile model with the Django admin site.
# Registering a model means Django will display it inside the /admin/ dashboard.
# From there, I can add, view, edit and delete client profile records.
# In this project, ClientProfile is important because it stores the client's basic identity and contact information.
# This supports the wider "know your client" part of the portfolio suitability workflow.
admin.site.register(FinancialProfile)
# This registers the FinancialProfile model with the Django admin site.
# This means financial profile records can be managed directly from /admin/.
# The FinancialProfile model stores information such as income, net worth, liabilities, liquidity needs and investment experience.
# In the wider application, this financial information helps support the suitability review before an investment mandate is approved.
# This also shows how Django connects models, database tables and the admin interface together.
admin.site.register(RiskAssessment)
# This registers the RiskAssessment model with the Django admin site.
# This allows risk assessment records to be checked and managed through the admin dashboard.
# The RiskAssessment model is linked to the suitability process because it helps record a client's risk tolerance and risk capacity.
# In the wider project workflow, this supports the decision about whether a mandate is suitable for a client.
# By registering this model, I can quickly inspect whether risk assessment data is being saved correctly in the database.