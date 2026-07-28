from django.apps import AppConfig
# This imports AppConfig from Django, which is the base class used to configure each Django app in the project.

class MandatesConfig(AppConfig):
    # This creates the configuration class for the mandates app.
    # Django uses this class to understand how the mandates app should be registered and loaded inside the wider project.
    default_auto_field = "django.db.models.BigAutoField"
    # This tells Django what type of automatic primary key field to use for models in this app.
    # BigAutoField creates large integer ID fields automatically, for example id = 1, 2, 3, and so on.
    # This matters because models such as InvestmentMandate, PortfolioHolding and PortfolioReviewProject will each need a unique database ID.
    name = "mandates"
    # This tells Django the internal name of the app.
    # The name must match the folder name, which is mandates.
    # Django uses this when the app is added to INSTALLED_APPS in settings.py.
    # This connects the mandates folder to the wider Django framework so its models, migrations, admin setup and views can be recognised.