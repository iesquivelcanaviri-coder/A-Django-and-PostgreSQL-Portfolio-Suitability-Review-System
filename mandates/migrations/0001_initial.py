from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL), ('clients', '0001_initial')]
    operations = [
        migrations.CreateModel(
            name='AssetCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True)),
                ('description', models.TextField(blank=True)),
                ('risk_level', models.CharField(blank=True, max_length=40)),
            ],
            options={'ordering': ['name']},
        ),
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=120)),
                ('model_name', models.CharField(max_length=80)),
                ('object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('description', models.TextField(blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-timestamp']},
        ),
        migrations.CreateModel(
            name='InvestmentMandate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mandate_name', models.CharField(max_length=180)),
                ('objective', models.CharField(max_length=255)),
                ('mandate_type', models.CharField(choices=[('ADVISORY', 'Advisory'), ('DISCRETIONARY', 'Discretionary')], max_length=30)),
                ('base_currency', models.CharField(default='EUR', max_length=10)),
                ('benchmark', models.CharField(blank=True, max_length=80)),
                ('expected_return_range', models.CharField(blank=True, max_length=80)),
                ('maximum_position_weight', models.DecimalField(decimal_places=2, default=10, max_digits=5)),
                ('esg_preference', models.CharField(blank=True, max_length=120)),
                ('product_restriction', models.CharField(blank=True, max_length=180)),
                ('liquidity_requirement', models.CharField(blank=True, max_length=120)),
                ('status', models.CharField(choices=[('DRAFT', 'Draft'), ('SUBMITTED', 'Submitted for Review'), ('MORE_INFO', 'More Information Required'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected'), ('CLOSED', 'Closed')], default='DRAFT', max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mandates_approved', to=settings.AUTH_USER_MODEL)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mandates', to='clients.clientprofile')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mandates_created', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-updated_at']},
        ),
        migrations.CreateModel(
            name='PortfolioHolding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('ticker', models.CharField(blank=True, max_length=20)),
                ('target_weight', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('current_weight', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('currency', models.CharField(default='EUR', max_length=10)),
                ('risk_notes', models.TextField(blank=True)),
                ('suitability_notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('asset_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mandates.assetcategory')),
                ('mandate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='holdings', to='mandates.investmentmandate')),
            ],
            options={'ordering': ['-current_weight'], 'unique_together': {('mandate', 'ticker')}},
        ),
        migrations.CreateModel(
            name='PortfolioReviewProject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=180)),
                ('description', models.TextField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('status', models.CharField(choices=[('PLANNED', 'Planned'), ('IN_PROGRESS', 'In Progress'), ('BLOCKED', 'Blocked'), ('COMPLETE', 'Complete'), ('ARCHIVED', 'Archived')], default='PLANNED', max_length=30)),
                ('priority', models.CharField(default='Medium', max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_projects', to='clients.clientprofile')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='projects_created', to=settings.AUTH_USER_MODEL)),
                ('mandate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='review_projects', to='mandates.investmentmandate')),
            ],
            options={'ordering': ['-start_date']},
        ),
        migrations.CreateModel(
            name='Stakeholder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stakeholder_role', models.CharField(max_length=80)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mandates.portfolioreviewproject')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={'unique_together': {('project', 'user')}},
        ),
        migrations.AddField(
            model_name='portfolioreviewproject',
            name='stakeholders',
            field=models.ManyToManyField(related_name='portfolio_projects', through='mandates.Stakeholder', to=settings.AUTH_USER_MODEL),
        ),
    ]
