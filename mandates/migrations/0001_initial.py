from django.conf import settings
# Imports the Django settings file, mainly so this migration can refer to the active user model used in the project.
from django.db import migrations, models
# Imports Django's migration tools and model field definitions, which are needed to describe the database tables.
import django.db.models.deletion
# Imports the deletion behaviours such as CASCADE and SET_NULL, which control what happens when related records are deleted.

class Migration(migrations.Migration):
    # Defines this file as a Django migration class, so Django knows it contains database changes to apply.
    initial = True
    # Marks this as the first migration for the mandates app, meaning it creates the first database structure for this app.
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL), ('clients', '0001_initial')]
    # This migration depends on the user model and the first clients migration because mandates connect to users and clients.
    operations = [
        # This list contains all the database operations Django will run when applying this migration.
        migrations.CreateModel(
            # Creates a new database table for the AssetCategory model.
            name='AssetCategory',
            # This is the Django model name, and Django will create a table for asset categories.
            fields=[
                # Starts the list of fields/columns that will belong to the AssetCategory table.
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                # Creates the automatic primary key ID field, which uniquely identifies each asset category record.
                ('name', models.CharField(max_length=80, unique=True)),
                # Stores the category name, such as Equities, Bonds, Cash or ETFs, and unique=True prevents duplicate category names.
                ('description', models.TextField(blank=True)),
                # Stores a longer explanation of the asset category, and blank=True means this field is optional in forms.
                ('risk_level', models.CharField(blank=True, max_length=40)),
                # Stores a simple risk label for the category, such as Low, Medium or High, and it can be left empty.
            ],
            options={'ordering': ['name']},
            # Orders asset categories alphabetically by name when they are queried from the database.
        ),
        
        migrations.CreateModel(
            # Creates a new database table for the AuditLog model.
            name='AuditLog',
            # This is the model used to store important governance actions in the system.
            fields=[
                # Starts the list of fields/columns for the AuditLog table.
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                # Creates the automatic primary key ID field for each audit log record.
                ('action', models.CharField(max_length=120)),
                # Stores the type of action that happened, such as created, updated, approved or rejected.
                ('model_name', models.CharField(max_length=80)),
                # Stores the name of the model affected by the action, which helps identify what part of the system changed.
                ('object_id', models.PositiveIntegerField(blank=True, null=True)),
                # Stores the ID of the object affected by the action, and blank/null allow it to be optional.
                ('description', models.TextField(blank=True)),
                # Stores extra details about the action, which helps explain the evidence trail in plain English.
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                # Automatically records the date and time when the audit log was first created.
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                # Links the audit action to a user, but SET_NULL keeps the audit record even if the user account is deleted.
            ],
        
            options={'ordering': ['-timestamp']},
            # Orders audit records by newest first, which is useful because recent actions usually matter most.
        ),
        
        migrations.CreateModel(
            # Creates a new database table for the InvestmentMandate model.
            name='InvestmentMandate',
            # This model stores the main investment mandate agreed for a client.
            fields=[
                # Starts the list of database fields for the InvestmentMandate table.
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                # Creates the automatic primary key ID field for each investment mandate.
                ('mandate_name', models.CharField(max_length=180)),
                # Stores the name of the mandate so users can identify it clearly in the system.
                ('objective', models.CharField(max_length=255)),
                # Stores the main investment objective, such as growth, income, preservation or balanced return.
                ('mandate_type', models.CharField(choices=[('ADVISORY', 'Advisory'), ('DISCRETIONARY', 'Discretionary')], max_length=30)),
                # Stores the type of mandate using choices, so users select either Advisory or Discretionary instead of typing freely.
                ('base_currency', models.CharField(default='EUR', max_length=10)),
                # Stores the main currency for the mandate, with EUR as the default value.
                ('benchmark', models.CharField(blank=True, max_length=80)),
                # Stores the benchmark used to compare performance, and it is optional because not every review needs one.
                ('expected_return_range', models.CharField(blank=True, max_length=80)),
                # Stores an educational expected return range, but as text because this project does not calculate real investment advice.
                ('maximum_position_weight', models.DecimalField(decimal_places=2, default=10, max_digits=5)),
                # Stores the maximum allowed weight for one position, helping show portfolio concentration control.
                ('esg_preference', models.CharField(blank=True, max_length=120)),
                # Stores any ESG preference, such as sustainability-focused or exclusion-based preferences.
                ('product_restriction', models.CharField(blank=True, max_length=180)),
                # Stores any restricted products, for example no derivatives or no high-risk products.
                ('liquidity_requirement', models.CharField(blank=True, max_length=120)),
                # Stores liquidity needs, which helps connect the mandate to the client's suitability profile.
                ('status', models.CharField(choices=[('DRAFT', 'Draft'), ('SUBMITTED', 'Submitted for Review'), ('MORE_INFO', 'More Information Required'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected'), ('CLOSED', 'Closed')], default='DRAFT', max_length=30)),
                # Stores the workflow status of the mandate and limits the value to controlled choices.
                ('created_at', models.DateTimeField(auto_now_add=True)),
                # Automatically stores when the mandate was first created.
                ('updated_at', models.DateTimeField(auto_now=True)),
                # Automatically updates the date and time whenever the mandate record is saved.
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mandates_approved', to=settings.AUTH_USER_MODEL)),
                # Links the mandate to the user who approved it, while SET_NULL keeps the mandate if that user is deleted.
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mandates', to='clients.clientprofile')),
                # Links the mandate to a client profile, and CASCADE deletes the mandates if the related client is deleted.
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mandates_created', to=settings.AUTH_USER_MODEL)),
                # Links the mandate to the user who created it, but keeps the mandate if that user account is removed.
            ],

            options={'ordering': ['-updated_at']},
            # Orders mandates by most recently updated first, which helps users see active/recent work at the top.
        ),
        
        migrations.CreateModel(
            # Creates a new database table for the PortfolioHolding model.
            name='PortfolioHolding',
            # This model stores individual holdings inside an investment mandate.
            fields=[
                # Starts the list of fields/columns for the PortfolioHolding table.
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                # Creates the automatic primary key ID field for each holding.
                ('name', models.CharField(max_length=150)),
                # Stores the name of the holding, such as a company, fund, bond or cash position.
                ('ticker', models.CharField(blank=True, max_length=20)),
                # Stores the ticker symbol if available, and blank=True allows holdings without a ticker.
                ('target_weight', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                # Stores the planned portfolio weight for this holding, such as 10.00 percent.
                ('current_weight', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                # Stores the current portfolio weight, which can be compared with the target weight.
                ('currency', models.CharField(default='EUR', max_length=10)),
                # Stores the currency of the holding, using EUR as the default.
                ('risk_notes', models.TextField(blank=True)),
                # Stores notes about risks linked to the holding, such as concentration, volatility or liquidity concerns.
                ('suitability_notes', models.TextField(blank=True)),
                # Stores notes explaining why the holding may or may not fit the client's mandate.
                ('created_at', models.DateTimeField(auto_now_add=True)),
                # Automatically records when the holding was first added.
                ('updated_at', models.DateTimeField(auto_now=True)),
                # Automatically updates the timestamp whenever the holding is changed.
                ('asset_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mandates.assetcategory')),
                # Links the holding to an asset category, but SET_NULL keeps the holding if the category is deleted.
                ('mandate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='holdings', to='mandates.investmentmandate')),
                # Links the holding to an investment mandate, and CASCADE deletes holdings if the mandate is deleted.
            ],

            options={'ordering': ['-current_weight'], 'unique_together': {('mandate', 'ticker')}},
            # Orders holdings by highest current weight first and prevents duplicate tickers inside the same mandate.
        ),
        
        migrations.CreateModel(
            # Creates a new database table for the PortfolioReviewProject model.
            name='PortfolioReviewProject',
            # This model represents a portfolio review project required by the assignment brief.
            fields=[
                # Starts the list of fields/columns for the PortfolioReviewProject table.
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                # Creates the automatic primary key ID field for each review project.
                ('project_name', models.CharField(max_length=180)),
                # Stores the project name, which helps identify the review.
                ('description', models.TextField()),
                # Stores the detailed project description, explaining the purpose of the review.
                ('start_date', models.DateField()),
                # Stores the project start date.
                ('end_date', models.DateField()),
                # Stores the project end date.
                ('status', models.CharField(choices=[('PLANNED', 'Planned'), ('IN_PROGRESS', 'In Progress'), ('BLOCKED', 'Blocked'), ('COMPLETE', 'Complete'), ('ARCHIVED', 'Archived')], default='PLANNED', max_length=30)),
                # Stores the project workflow status using controlled choices instead of free text.
                ('priority', models.CharField(default='Medium', max_length=30)),
                # Stores the project priority, with Medium as the default value.
                ('created_at', models.DateTimeField(auto_now_add=True)),
                # Automatically records when the project was created.
                ('updated_at', models.DateTimeField(auto_now=True)),
                # Automatically updates when the project record is changed.
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_projects', to='clients.clientprofile')),
                # Links the review project to a client, and CASCADE removes the project if the client is deleted.
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='projects_created', to=settings.AUTH_USER_MODEL)),
                # Links the project to the user who created it, while keeping the project if that user is deleted.
                ('mandate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='review_projects', to='mandates.investmentmandate')),
                # Optionally links the review project to an investment mandate, and SET_NULL keeps the project if the mandate is removed.
            ],
        
            options={'ordering': ['-start_date']},
            # Orders projects by newest start date first, so recent review work appears first.
        ),
    
        migrations.CreateModel(
            # Creates a new database table for the Stakeholder model.
            name='Stakeholder',
            # This model connects users to portfolio review projects with a specific project role.
            fields=[
                # Starts the list of fields/columns for the Stakeholder table.
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                # Creates the automatic primary key ID field for each stakeholder record.
                ('stakeholder_role', models.CharField(max_length=80)),
                # Stores the role of the user in the project, such as Adviser, Reviewer or Compliance Officer.
                ('date_added', models.DateTimeField(auto_now_add=True)),
                # Automatically records when the stakeholder was added to the project.
                ('is_active', models.BooleanField(default=True)),
                # Stores whether the stakeholder is still active on the project.
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mandates.portfolioreviewproject')),
                # Links the stakeholder record to a portfolio review project, and CASCADE removes it if the project is deleted.
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                # Links the stakeholder record to a Django user, and CASCADE removes it if the user is deleted.
            ],
    
            options={'unique_together': {('project', 'user')}},
            # Prevents the same user from being added to the same project more than once.
        ),

        migrations.AddField(
            # Adds a ManyToManyField to PortfolioReviewProject after the Stakeholder model has been created.
            model_name='portfolioreviewproject',
            # Specifies that the new field will be added to the PortfolioReviewProject model.
            name='stakeholders',
            # Names the new field stakeholders, which allows each project to have multiple users involved.
            field=models.ManyToManyField(related_name='portfolio_projects', through='mandates.Stakeholder', to=settings.AUTH_USER_MODEL),
            # Creates a many-to-many relationship between projects and users through the Stakeholder model.
        ),
    ]