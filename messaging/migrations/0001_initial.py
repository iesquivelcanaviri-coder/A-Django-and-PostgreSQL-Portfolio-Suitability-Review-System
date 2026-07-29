from django.conf import settings
# Imports the Django project settings, so this migration can refer to the active user model instead of hardcoding a user table.
from django.db import migrations, models
# Imports Django's migration tools and model field types, which are needed to describe the database table structure.
import django.db.models.deletion
# Imports Django's deletion behaviours, such as CASCADE and SET_NULL, for ForeignKey relationships.

class Migration(migrations.Migration):
    # Defines a migration class. Django reads this class to know what database changes must be applied.
    initial = True
    # Marks this as the first migration for the messaging app, meaning it creates the first database structure for this app.
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL), ('mandates', '0001_initial')]
    # Tells Django this migration depends on two things before it can run:
    # 1. The active User model must already exist.
    # 2. The first migration in the mandates app must already exist, because Message links to PortfolioReviewProject.
    operations = [
        # Starts the list of database actions Django must perform when this migration is applied.
        migrations.CreateModel(
            # Creates a new database table based on a Django model.
            name='Message',
            # Names the model being created. Django will create a database table for the Message model.
            fields=[
                # Starts the list of fields/columns that will exist in the Message table.
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                # Creates the automatic primary key column.
                # BigAutoField is an auto-incrementing integer field.
                # primary_key=True means each message gets a unique ID.
                ('subject', models.CharField(max_length=180)),
                # Creates the message subject field.
                # CharField is used for shorter text.
                # max_length=180 limits the subject so it does not become too long.
                ('body', models.TextField()),
                # Creates the main message body field.
                # TextField is used because the message content can be longer than a short title.
                ('sent_at', models.DateTimeField(auto_now_add=True)),
                # Stores the date and time when the message is created.
                # auto_now_add=True means Django automatically fills this once when the message is first saved.
                ('is_read', models.BooleanField(default=False)),
                # Stores whether the recipient has read the message.
                # It starts as False because a new message is unread when first created.
                ('sender_archived', models.BooleanField(default=False)),
                # Tracks whether the sender archived the message from their sent messages view.
                # This does not delete the message for everyone; it only hides it from the sender side.
                ('recipient_archived', models.BooleanField(default=False)),
                # Tracks whether the recipient archived the message from their inbox.
                # This supports inbox archive functionality without immediately deleting the database record.
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to=settings.AUTH_USER_MODEL)),
                # Creates a ForeignKey relationship to the user who receives the message.
                # to=settings.AUTH_USER_MODEL links to Django's active user model.
                # on_delete=CASCADE means if the recipient user is deleted, their received messages are also deleted.
                # related_name='received_messages' lets Django access messages received by a user using user.received_messages.all().
                ('related_project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='messages', to='mandates.portfolioreviewproject')),
                # Creates an optional link between a message and a PortfolioReviewProject from the mandates app.
                # blank=True allows the form to be submitted without selecting a project.
                # null=True allows the database column to store NULL when there is no related project.
                # on_delete=SET_NULL means if the project is deleted, the message stays but its project link becomes empty.
                # related_name='messages' lets Django access all messages for a project using project.messages.all().
                # This connects the messaging app to the wider portfolio review workflow.
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to=settings.AUTH_USER_MODEL)),
                # Creates a ForeignKey relationship to the user who sends the message.
                # on_delete=CASCADE means if the sender user is deleted, their sent messages are also deleted.
                # related_name='sent_messages' lets Django access messages sent by a user using user.sent_messages.all().
                # This is how the app separates inbox messages from sent messages.
            ],
            options={'ordering': ['-sent_at']},
            # Sets the default ordering for messages.
            # '-sent_at' means newest messages appear first, which is useful for inbox and sent message pages.
        ),
    
    ]
    