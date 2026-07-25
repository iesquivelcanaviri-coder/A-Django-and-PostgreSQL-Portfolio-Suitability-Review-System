# ==========================================================
#  ADMIN CONFIGURATION FOR USER PROFILES
# ==========================================================
# This file controls how the UserProfile model appears inside
# the Django admin panel. The admin panel is a built-in Django
# feature that lets the site owner manage database records
# without writing separate views, templates, or forms manually.

from django.contrib import admin  # Imports Django's built-in admin module, which provides the ready-made admin dashboard for managing database models.

from .models import UserProfile  # Imports the UserProfile model from the current app's models.py file so it can be registered and managed in the admin panel.


# ----------------------------------------------------------
#  REGISTERING THE USERPROFILE MODEL WITH THE ADMIN SITE
# ----------------------------------------------------------
# The @admin.register(UserProfile) decorator tells Django:
# "Show this model inside the admin panel and use the custom
# admin settings written in the class below."
#
# This is a cleaner version of writing:
# admin.site.register(UserProfile, UserProfileAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    # This class customises how UserProfile records are displayed
    # in the Django admin interface. It inherits from admin.ModelAdmin,
    # which is Django's base class for controlling admin behaviour.

    list_display = ("user", "role", "phone", "organisation", "updated_at")
    # list_display controls which columns appear in the admin list view.
    # Instead of only seeing "UserProfile object", the admin can quickly see
    # the related user, their role, phone number, organisation, and last update.
    # This is useful because UserProfile supports the role-based part of the app.

    list_filter = ("role",)
    # list_filter adds a filter sidebar in the admin panel.
    # In this case, the admin can filter users by role, such as Client,
    # Adviser, Portfolio Manager, Compliance Reviewer, or Admin.
    # This connects to the wider app because different roles control what users
    # are allowed to do, especially around mandate approval and private access.

    search_fields = ("user__username", "user__email", "organisation")
    # search_fields adds a search box to the admin page.
    # The double underscore syntax, such as user__username, is Django ORM syntax.
    # It means: search inside the related User model and look at its username field.
    # user__email works the same way, but searches the linked user's email.
    # organisation searches directly inside the UserProfile model.
    # This shows how Django can search across related database tables using ORM relationships.