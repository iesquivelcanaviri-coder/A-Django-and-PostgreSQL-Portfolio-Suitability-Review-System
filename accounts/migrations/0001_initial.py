# Generated for SuitabilityDesk assignment project.
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('CLIENT', 'Client'), ('ADVISER', 'Adviser'), ('PORTFOLIO_MANAGER', 'Portfolio Manager'), ('COMPLIANCE', 'Compliance Reviewer'), ('ADMIN', 'Administrator')], default='CLIENT', max_length=30)),
                ('phone', models.CharField(blank=True, max_length=40)),
                ('organisation', models.CharField(blank=True, max_length=150)),
                ('job_title', models.CharField(blank=True, max_length=120)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
