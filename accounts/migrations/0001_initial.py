# Generated for SuitabilityDesk assignment project.
# This comment explains that this migration file belongs to my SuitabilityDesk Django project and was created to set up the first database table for the accounts app.
from django.conf import settings
# This imports the Django settings file, which is important because the project settings tell Django which user model is being used.
from django.db import migrations, models
# This imports Django's migration tools and model field tools, so this file can describe database changes such as creating a new table.
import django.db.models.deletion
# This imports Django's deletion behaviour options, which are used below for the relationship between UserProfile and the User table.

class Migration(migrations.Migration):
    # This defines a migration class, and Django reads this class when it needs to apply database changes.
    initial = True
    # This means this is the first migration for the accounts app, so it creates the starting database structure for this app.
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    # This tells Django that this migration depends on the user model existing first, because UserProfile links to Django's built-in User table.
    operations = [
        # This list contains the actual database operations Django must run, such as creating tables or adding fields.
        migrations.CreateModel(
            # This operation tells Django to create a new database table based on a model.
            name='UserProfile',
            # This is the name of the Django model being created, and it will become a database table called something like accounts_userprofile.
            fields=[
                # This list defines the columns that will exist in the UserProfile database table.
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                # This creates the automatic primary key column for the table, so each user profile has a unique ID in the database.
                ('role', models.CharField(choices=[('CLIENT', 'Client'), ('ADVISER', 'Adviser'), ('PORTFOLIO_MANAGER', 'Portfolio Manager'), ('COMPLIANCE', 'Compliance Reviewer'), ('ADMIN', 'Administrator')], default='CLIENT', max_length=30)),
                # This creates a text field for the user's role, using fixed choices so the system can control permissions such as client, adviser, portfolio manager, compliance reviewer or admin.
                ('phone', models.CharField(blank=True, max_length=40)),
                # This creates a phone number field, and blank=True means the user can leave it empty if they do not want to add a phone number.
                ('organisation', models.CharField(blank=True, max_length=150)),
                # This creates an organisation field, which is useful for recording where the user works or what organisation they are connected to.
                ('job_title', models.CharField(blank=True, max_length=120)),
                # This creates a job title field, which helps make the profile more realistic for a portfolio suitability review system.
                ('created_at', models.DateTimeField(auto_now_add=True)),
                # This automatically stores the date and time when the profile is first created, which is useful for audit and database tracking.
                ('updated_at', models.DateTimeField(auto_now=True)),
                # This automatically updates the date and time whenever the profile record is changed, which helps show when the user profile was last edited.
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
                # This links each UserProfile to exactly one Django user, and CASCADE means the profile is deleted if the linked user is deleted.
            ],
        ),
        
    ]
    