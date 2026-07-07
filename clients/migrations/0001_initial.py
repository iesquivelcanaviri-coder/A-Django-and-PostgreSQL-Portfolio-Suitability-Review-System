from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(
            name='ClientProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=180)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(blank=True, max_length=40)),
                ('address', models.CharField(blank=True, max_length=255)),
                ('tax_residency', models.CharField(blank=True, max_length=120)),
                ('client_type', models.CharField(choices=[('INDIVIDUAL', 'Individual'), ('CORPORATE', 'Corporate'), ('FAMILY_OFFICE', 'Family Office'), ('TRUST', 'Trust')], default='INDIVIDUAL', max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='clients_created', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='client_record', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['full_name']},
        ),
        migrations.CreateModel(
            name='FinancialProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('net_worth', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('existing_investments', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('liabilities', models.DecimalField(decimal_places=2, default=0, max_digits=14)),
                ('income_band', models.CharField(blank=True, max_length=80)),
                ('investment_experience', models.CharField(blank=True, max_length=120)),
                ('liquidity_need', models.CharField(choices=[('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High'), ('MONTHLY', 'Monthly liquidity required')], default='MEDIUM', max_length=30)),
                ('time_horizon_years', models.PositiveIntegerField(default=5)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('client', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='financial_profile', to='clients.clientprofile')),
            ],
        ),
        migrations.CreateModel(
            name='RiskAssessment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('risk_tolerance', models.CharField(choices=[('VERY_LOW', 'Very Low'), ('CONSERVATIVE', 'Conservative'), ('BALANCED', 'Balanced'), ('GROWTH', 'Growth'), ('AGGRESSIVE', 'Aggressive')], max_length=30)),
                ('risk_capacity', models.CharField(choices=[('VERY_LOW', 'Very Low'), ('CONSERVATIVE', 'Conservative'), ('BALANCED', 'Balanced'), ('GROWTH', 'Growth'), ('AGGRESSIVE', 'Aggressive')], max_length=30)),
                ('max_drawdown_percent', models.IntegerField(default=-15)),
                ('loss_reaction', models.CharField(blank=True, max_length=255)),
                ('assessment_score', models.PositiveIntegerField(default=0)),
                ('outcome', models.CharField(choices=[('SUITABLE', 'Suitable'), ('NEEDS_REVIEW', 'Needs Review'), ('UNSUITABLE', 'Potentially Unsuitable')], default='NEEDS_REVIEW', max_length=30)),
                ('review_due_date', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('assessed_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='risk_assessments', to='clients.clientprofile')),
            ],
            options={'ordering': ['-created_at']},
        ),
    ]
