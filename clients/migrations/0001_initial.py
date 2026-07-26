from django.conf import settings
# This imports the Django settings file, so the migration can refer to project settings such as the active User model.
from django.db import migrations, models
# This imports Django's migration tools and model field types, which are needed to describe database table changes.
import django.db.models.deletion
# This imports Django's deletion behaviours, such as CASCADE and SET_NULL, used for ForeignKey and OneToOneField relationships.

class Migration(migrations.Migration):
    # This class represents one database migration file.
    # Django reads this class to know what database tables and fields need to be created.
    initial = True
    # This tells Django that this is the first migration for the clients app.
    # It usually creates the first version of the database tables for this app.
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    # This means this migration depends on the User model existing first.
    # settings.AUTH_USER_MODEL is used instead of directly writing auth.User, which keeps the project flexible if a custom user model is used later.
    operations = [
        # The operations list contains the database actions Django will perform.
        # In this file, the main action is creating three database tables: ClientProfile, FinancialProfile and RiskAssessment.
        migrations.CreateModel(
            # This operation tells Django to create a new database table for the ClientProfile model.
            name='ClientProfile',
            # This is the name of the Django model being created.
            # Django will normally create a database table called clients_clientprofile.
            fields=[
                # The fields list defines each database column inside the ClientProfile table.
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                # This creates the automatic primary key field for each client profile.
                # BigAutoField means Django creates a large auto-incrementing integer ID.
                ('full_name', models.CharField(max_length=180)),
                # This stores the client's full name as text.
                # CharField is used because the value has a maximum length.
                ('email', models.EmailField(max_length=254)),
                # This stores the client's email address.
                # EmailField gives basic email-format validation at the Django/form level.
                ('phone', models.CharField(blank=True, max_length=40)),
                # This stores the client's phone number.
                # blank=True means the field can be left empty in forms.
                ('address', models.CharField(blank=True, max_length=255)),
                # This stores the client's address.
                # It is optional because blank=True is included.
                ('tax_residency', models.CharField(blank=True, max_length=120)),
                # This stores the client's tax residency.
                # This is useful in a portfolio suitability system because tax residency can affect client records and review information.
                ('client_type', models.CharField(choices=[('INDIVIDUAL', 'Individual'), ('CORPORATE', 'Corporate'), ('FAMILY_OFFICE', 'Family Office'), ('TRUST', 'Trust')], default='INDIVIDUAL', max_length=30)),
                # This stores the type of client.
                # choices restricts the allowed values to Individual, Corporate, Family Office or Trust.
                # default='INDIVIDUAL' means a new client is treated as an individual unless another type is selected.
                ('created_at', models.DateTimeField(auto_now_add=True)),
                # This automatically stores the date and time when the client profile is first created.
                # auto_now_add=True is useful for audit/history evidence.
                ('updated_at', models.DateTimeField(auto_now=True)),
                # This automatically updates the date and time whenever the client profile is changed.
                # This helps show when client details were last reviewed or edited.
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='clients_created', to=settings.AUTH_USER_MODEL)),
                # This links the client profile to the user who created it.
                # ForeignKey means many client records can be created by one user.
                # null=True allows the field to become empty if needed.
                # SET_NULL means if the user is deleted, the client profile is kept but created_by becomes NULL.
                # related_name='clients_created' allows reverse access, such as user.clients_created.all().
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='client_record', to=settings.AUTH_USER_MODEL)),
                # This optionally links a client profile to one Django user account.
                # OneToOneField means one user can only have one linked client record.
                # blank=True and null=True make the link optional.
                # SET_NULL keeps the client profile if the linked user account is deleted.
                # related_name='client_record' allows reverse access, such as user.client_record.
            ],
            options={'ordering': ['full_name']},
            # This sets the default ordering for ClientProfile query results.
            # When clients are listed, they will normally appear alphabetically by full_name.
        ),
        migrations.CreateModel(
            # This operation creates the FinancialProfile model/table.
            # It stores the client's financial background used for suitability review.
            name='FinancialProfile',
            # This is the Django model name.
            # Django will usually create a table called clients_financialprofile.
            fields=[
                # These fields become database columns in the FinancialProfile table.
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                # This creates the automatic primary key for each financial profile record.
                ('net_worth', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                # This stores the client's net worth as a decimal number.
                # DecimalField is better than FloatField for money because it avoids floating-point rounding issues.
                # max_digits=14 allows large amounts, while decimal_places=2 allows cents/pence-style values.
                ('existing_investments', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                # This stores the value of the client's existing investments.
                # It supports suitability analysis by showing what the client already has invested.
                ('liabilities', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                # This stores the client's debts or financial obligations.
                # Liabilities are important because they can reduce risk capacity.
                ('income_band', models.CharField(blank=True, max_length=80)),
                # This stores a general income category or income range.
                # It is optional because blank=True is included.
                ('investment_experience', models.CharField(blank=True, max_length=120)),
                # This stores the client's investment knowledge or experience level.
                # It helps support the wider suitability process.
                ('liquidity_need', models.CharField(choices=[('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High'), ('MONTHLY', 'Monthly liquidity required')], default='MEDIUM', max_length=30)),
                # This records how much access to cash or liquid assets the client needs.
                # choices controls the allowed values.
                # default='MEDIUM' gives a sensible starting value when no specific option is selected.
                ('time_horizon_years', models.PositiveIntegerField(default=5)),
                # This stores the client's investment time horizon in years.
                # PositiveIntegerField prevents negative values.
                # A longer time horizon may support more growth-focused investment choices in a suitability workflow.
                ('created_at', models.DateTimeField(auto_now_add=True)),
                # This records when the financial profile was first created.
                ('updated_at', models.DateTimeField(auto_now=True)),
                # This records when the financial profile was last updated.
                ('client', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='financial_profile', to='clients.clientprofile')),
                # This links the financial profile to exactly one client profile.
                # OneToOneField means each client should only have one financial profile.
                # CASCADE means if the client profile is deleted, the financial profile is deleted too.
                # related_name='financial_profile' allows access like client.financial_profile.
            ],
        ),
        migrations.CreateModel(
            # This operation creates the RiskAssessment model/table.
            # It stores the suitability and risk review outcome for a client.
            name='RiskAssessment',
            # This is the Django model name.
            # Django will normally create a table called clients_riskassessment.
            fields=[
                # These fields define the database columns for the RiskAssessment table.
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                # This creates the automatic primary key for each risk assessment.
                ('risk_tolerance', models.CharField(choices=[('VERY_LOW', 'Very Low'), ('CONSERVATIVE', 'Conservative'), ('BALANCED', 'Balanced'), ('GROWTH', 'Growth'), ('AGGRESSIVE', 'Aggressive')], max_length=30)),
                # This stores how much risk the client is emotionally or personally willing to accept.
                # choices limit the values to a controlled risk scale.
                ('risk_capacity', models.CharField(choices=[('VERY_LOW', 'Very Low'), ('CONSERVATIVE', 'Conservative'), ('BALANCED', 'Balanced'), ('GROWTH', 'Growth'), ('AGGRESSIVE', 'Aggressive')], max_length=30)),
                # This stores how much risk the client can financially afford to take.
                # This is different from risk tolerance because someone may want high risk but not have the financial capacity for it.
                ('max_drawdown_percent', models.IntegerField(default=-15)),
                # This stores the maximum portfolio fall the client may be able to tolerate.
                # The default is -15, meaning a 15% loss scenario is used as a starting assumption.
                ('loss_reaction', models.CharField(blank=True, max_length=255)),
                # This stores notes about how the client may react to investment losses.
                # It is optional because blank=True is included.
                ('assessment_score', models.PositiveIntegerField(default=0)),
                # This stores a simple numerical score for the risk assessment.
                # PositiveIntegerField means the score cannot be negative.
                ('outcome', models.CharField(choices=[('SUITABLE', 'Suitable'), ('NEEDS_REVIEW', 'Needs Review'), ('UNSUITABLE', 'Potentially Unsuitable')], default='NEEDS_REVIEW', max_length=30)),
                # This stores the result of the suitability assessment.
                # choices keep the outcome controlled and consistent.
                # default='NEEDS_REVIEW' is cautious because a new assessment should be reviewed before being treated as suitable.
                ('review_due_date', models.DateField(blank=True, null=True)),
                # This stores the date when the risk assessment should be reviewed again.
                # blank=True allows forms to leave it empty.
                # null=True allows the database to store an empty value.
                ('created_at', models.DateTimeField(auto_now_add=True)),
                # This records when the risk assessment was created.
                ('updated_at', models.DateTimeField(auto_now=True)),
                # This records when the risk assessment was last updated.
                ('assessed_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                # This links the risk assessment to the user who assessed it.
                # ForeignKey is used because one staff user/adviser can assess many clients.
                # SET_NULL keeps the assessment record if the assessor account is deleted.
                # This supports an evidence trail without losing historical assessment records.
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='risk_assessments', to='clients.clientprofile')),
                # This links the risk assessment to the client profile.
                # ForeignKey allows one client to have many risk assessments over time.
                # CASCADE means if the client is deleted, the related risk assessments are deleted too.
                # related_name='risk_assessments' allows access like client.risk_assessments.all().
            ],

            options={'ordering': ['-created_at']},
            # This sets the default order for risk assessments.
            # The newest assessments appear first because of the minus sign before created_at.
        ),
    ]
# After this migration is applied, Django will create the three client-related database tables.