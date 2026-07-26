# ==========================================================
#  ADMIN CONFIGURATION FOR USER PROFILES
# ==========================================================
# This file controls how the UserProfile model appears inside
# the Django admin panel. The admin panel is a built-in Django
# feature that lets the site owner manage database records
# without writing separate views, templates, or forms manually.
# In this project, the admin panel is useful because it gives
# evidence that the UserProfile data is stored in the database
# and can be managed through Django's built-in framework tools.


from django.contrib import admin
# Imports Django's built-in admin module.
# The admin module gives the project a ready-made dashboard where models
# can be viewed, searched, filtered, added, edited and deleted.
# This connects to the wider Django framework because Django automatically
# provides this admin system once models are registered here.
from .models import UserProfile
# Imports the UserProfile model from the accounts app's models.py file.
# The dot before models means "look inside the current app folder".
# This is needed because Django cannot show the UserProfile table in the
# admin panel unless the model is imported and registered.
# In this project, UserProfile extends the built-in User model with extra
# details such as role, phone, organisation and job title.


# ----------------------------------------------------------
#  REGISTERING THE USERPROFILE MODEL WITH THE ADMIN SITE
# ----------------------------------------------------------
# The @admin.register(UserProfile) decorator tells Django:
# "Add the UserProfile model to the admin panel and use the custom
# admin settings written in the class below."
# This is a cleaner and more modern version of writing:
# admin.site.register(UserProfile, UserProfileAdmin)
# Registering the model is important because it makes the database table
# visible and manageable through the admin interface.
@admin.register(UserProfile)
# Registers the UserProfile model with Django's admin site.
# This means that when the admin user logs into /admin/, they can see
# and manage UserProfile records from the accounts app.
# The decorator also connects the model to the custom UserProfileAdmin
# class written below.
class UserProfileAdmin(admin.ModelAdmin):
    # Creates a custom admin configuration class for the UserProfile model.
    # The class inherits from admin.ModelAdmin, which is Django's built-in
    # base class for changing how a model behaves in the admin panel.
    # This class does not create a new database table. It only controls
    # how existing UserProfile records are displayed and managed in admin.
    list_display = ("user", "role", "phone", "organisation", "updated_at")
    # list_display controls which columns appear in the admin list view.
    # This makes the admin table much easier to read because it shows
    # important UserProfile information immediately.
    # "user" shows the linked Django User account.
    # "role" shows whether the person is a Client, Adviser, Portfolio Manager,
    # Compliance Reviewer or Admin.
    # "phone" and "organisation" help identify the user in a practical way.
    # "updated_at" shows when the profile was last changed.
    # This is useful for the wider application because UserProfile supports
    # role-based access and contact profile management.
    list_filter = ("role",)
    # list_filter adds a filter panel on the right side of the admin list page.
    # The comma after "role" is needed because Python treats this as a tuple.
    # Without the comma, it would just be a normal string.
    # This lets the admin quickly filter profiles by role.
    # For example, the admin can view only Clients, Advisers, Portfolio Managers,
    # Compliance Reviewers or Admin users.
    # This connects to the wider project because roles control what users can
    # do in the portfolio suitability workflow, especially actions such as
    # mandate approval and access to private dashboard features.
    search_fields = ("user__username", "user__email", "organisation")
    # search_fields adds a search box at the top of the UserProfile admin page.
    # This makes it easier to find a profile without scrolling through every user.
    # "user__username" uses Django ORM double-underscore syntax to search
    # the username field inside the related built-in User model.
    # "user__email" also searches inside the related User model, but checks
    # the email field instead.
    # "organisation" searches directly inside the UserProfile model itself.
    # This is a good example of how Django can follow model relationships
    # and search across connected database tables.
    # It also shows the connection between accounts_userprofile and auth_user
    # in the PostgreSQL database.