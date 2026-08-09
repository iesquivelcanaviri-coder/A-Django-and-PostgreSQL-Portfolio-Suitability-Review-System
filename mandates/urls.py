from django.urls import path
# This imports Django's path function, which is used to connect URL patterns to view functions.
from . import views
# This imports the views.py file from the same mandates app folder, so each URL can call the correct mandate view.

app_name = "mandates"
# This gives the mandates app its own URL namespace, which helps Django identify these URLs as belonging to the mandates app.
# Example: in templates, I can use {% url 'mandates:list' %} instead of only using 'list'.
# This is useful because other apps might also have views called list, create, detail, or update.

urlpatterns = [
# This list stores all the URL routes for the mandates app.
# Django reads this list to know which view should run when the user visits a specific URL.
    path("", views.mandate_list, name="list"),
    # This is the main mandates page.
    # The empty string "" means this route is the default page for the mandates app.
    # If the project-level urls.py includes this app at /mandates/, then this route becomes /mandates/.
    # It calls mandate_list from views.py, which should display all investment mandates.
    # The name="list" lets me refer to this URL in templates as {% url 'mandates:list' %}.
    path("new/", views.mandate_create, name="create"),
    # This route opens the page for creating a new investment mandate.
    # The final URL will usually be /mandates/new/.
    # It calls mandate_create from views.py, which should show a form and save a new mandate when submitted.
    # The name="create" lets me link to this page using {% url 'mandates:create' %}.
    path("projects/", views.project_list, name="projects"),
    # This route displays the portfolio review projects page.
    # The final URL will usually be /mandates/projects/.
    # It calls project_list from views.py, which should show review projects stored in the database.
    # This connects directly to the assignment requirement for storing project details such as name, dates, status and stakeholders.
    # The name="projects" lets me link to this page using {% url 'mandates:projects' %}.
    path("projects/new/", views.project_create, name="project_create"),
    # This route opens the form for creating a new portfolio review project.
    # The final URL will usually be /mandates/projects/new/.
    # It calls project_create from views.py, which should save a new review project to PostgreSQL.
    # This supports the project-management part of the application because users can create structured review projects.
    # The name="project_create" lets me link to this page using {% url 'mandates:project_create' %}.
    path("<int:pk>/", views.mandate_detail, name="detail"),
    # This route opens the detail page for one specific mandate.
    # <int:pk> means Django expects an integer primary key from the database.
    # Example: /mandates/3/ would show the mandate with primary key 3.
    # It calls mandate_detail from views.py, which should retrieve and display one mandate record.
    # The name="detail" lets me link to a mandate detail page using {% url 'mandates:detail' mandate.pk %}.
    path("<int:pk>/edit/", views.mandate_update, name="update"),
    # This route opens the edit page for one existing mandate.
    # <int:pk> tells Django which mandate record should be updated.
    # Example: /mandates/3/edit/ would edit the mandate with primary key 3.
    # It calls mandate_update from views.py, which should load the form with existing data and save changes.
    # The name="update" lets me create edit links using {% url 'mandates:update' mandate.pk %}.
    path("<int:pk>/approve/", views.mandate_approve, name="approve"),
    # This route is used to approve a specific mandate.
    # <int:pk> identifies which mandate is being approved.
    # Example: /mandates/3/approve/ would approve the mandate with primary key 3.
    # It calls mandate_approve from views.py, where role-based permission checks should happen.
    # This connects to the wider framework requirement for authorization because only allowed roles should approve mandates.
    # The name="approve" lets me create approval buttons using {% url 'mandates:approve' mandate.pk %}.
    path("holdings/new/", views.holding_create, name="holding_create"),
    # This route opens the page for creating a new portfolio holding.
    # The final URL will usually be /mandates/holdings/new/.
    # It calls holding_create from views.py, which should save a holding linked to a mandate or asset category.
    # This supports the assignment requirement to store and categorise user data in the database.
    # The name="holding_create" lets me link to this page using {% url 'mandates:holding_create' %}.
    path("holdings/<int:pk>/delete/", views.holding_delete, name="holding_delete"),
    # This route deletes a specific portfolio holding.
    # <int:pk> identifies which holding should be deleted from the database.
    # Example: /mandates/holdings/5/delete/ would target the holding with primary key 5.
    # It calls holding_delete from views.py, which should normally confirm the delete action before removing the record.
    # This is part of CRUD because it demonstrates the Delete operation.
    # The name="holding_delete" lets me create delete links using {% url 'mandates:holding_delete' holding.pk %}.

]
# After this, Django has all the route-to-view connections for the mandates app.