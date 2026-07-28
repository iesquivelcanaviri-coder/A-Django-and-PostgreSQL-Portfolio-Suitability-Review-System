from django.contrib import admin
# This imports Django's built-in admin system.
# The admin system gives the project a ready-made backend interface where I can view, add, edit and delete database records without building custom pages for everything.
from .models import AssetCategory, AuditLog, InvestmentMandate, PortfolioHolding, PortfolioReviewProject, Stakeholder
# This imports the models from the current app's models.py file.
# The dot before models means "look inside this same app folder", which in this case is the mandates app.
# These models represent the database tables connected to the portfolio suitability and mandate workflow.
# Importing them here allows Django admin to know which database tables I want to manage through the admin panel.

admin.site.register(AssetCategory)
# This registers the AssetCategory model with the Django admin site.
# It means I can manage asset categories, such as equities, bonds, ETFs or cash, from the admin dashboard.
# In the wider project, this helps categorise portfolio holdings properly instead of storing holdings without structure.
admin.site.register(AuditLog)
# This registers the AuditLog model with the Django admin site.
# The audit log is important because it records key governance actions, such as creating, updating, approving or rejecting records.
# In the wider framework, this supports accountability and shows an evidence trail for portfolio review decisions.
admin.site.register(InvestmentMandate)
# This registers the InvestmentMandate model with the Django admin site.
# An investment mandate stores the main portfolio rules, such as objective, benchmark, base currency, ESG preference, restrictions and approval status.
# Registering it here lets an admin user inspect and manage mandate records directly in the Django admin interface.
admin.site.register(PortfolioHolding)
# This registers the PortfolioHolding model with the Django admin site.
# Portfolio holdings are the individual assets linked to a mandate, such as shares, bonds, funds or cash positions.
# This connects to the database part of the project because each holding is saved as a proper PostgreSQL record instead of being temporary page data.
admin.site.register(PortfolioReviewProject)
# This registers the PortfolioReviewProject model with the Django admin site.
# This model supports the assignment requirement for storing project details such as project name, description, start date, end date, status and stakeholders.
# Registering it here makes it easier to check whether review projects are being saved correctly in the database.
admin.site.register(Stakeholder)
# This registers the Stakeholder model with the Django admin site.
# Stakeholders connect users to portfolio review projects with a role, such as adviser, reviewer, portfolio manager or compliance reviewer.
# This helps show the wider Django relationship structure because users, projects and roles are linked together through the database.