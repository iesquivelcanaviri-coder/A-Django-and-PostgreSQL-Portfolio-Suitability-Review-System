from django.urls import path
# This imports Django's path function, which is used to connect a URL pattern to a specific view function.
from . import views
# This imports the views.py file from the current clients app, so this urls.py file can call the client-related view functions.

app_name = "clients"
# This gives the clients app its own namespace, which helps Django identify these URLs separately from other apps.
# For example, in templates I can use {% url 'clients:list' %} instead of only using "list", which avoids confusion if another app also has a URL called "list".

urlpatterns = [
# This list stores all the URL routes for the clients app.
# Django reads this list and matches the user's browser URL to the correct view function.
    path("", views.client_list, name="list"),
    # This route is for the main clients page.
    # The empty string "" means this is the default page for the clients app, for example /clients/.
    # It connects to the client_list view in views.py.
    # The name "list" lets me refer to this route in templates as {% url 'clients:list' %}.
    path("new/", views.client_create, name="create"),
    # This route is for creating a new client.
    # The browser URL would be something like /clients/new/.
    # It connects to the client_create view, where the form for adding a client is handled.
    # The name "create" lets me link to it using {% url 'clients:create' %}.
    path("<int:pk>/", views.client_detail, name="detail"),
    # This route is for viewing one specific client's details.
    # <int:pk> means Django expects an integer in the URL, such as /clients/1/.
    # pk stands for primary key, which is the unique database ID for that client.
    # Django passes this pk value into the client_detail view so the correct client can be found from the database.
    # The name "detail" lets me link to a specific client using {% url 'clients:detail' client.pk %}.
    path("<int:pk>/edit/", views.client_update, name="update"),
    # This route is for editing an existing client.
    # The <int:pk> part tells Django which client record should be updated.
    # For example, /clients/3/edit/ would open the edit page for the client with primary key 3.
    # It connects to the client_update view, which normally loads the form with the existing client data.
    # The name "update" lets me create edit links using {% url 'clients:update' client.pk %}.
    path("<int:client_pk>/financial/", views.financial_profile_edit, name="financial"),
    # This route is for creating or editing a financial profile linked to a specific client.
    # <int:client_pk> is used instead of pk to make it clearer that the number belongs to a ClientProfile record.
    # For example, /clients/2/financial/ would open the financial profile page for client 2.
    # This connects to the financial_profile_edit view, where income, net worth, liabilities or liquidity information can be handled.
    # The name "financial" lets me link to this page using {% url 'clients:financial' client.pk %}.
    path("risk/new/", views.risk_assessment_create, name="risk_create"),
    # This route is for creating a new risk assessment.
    # The URL would be /clients/risk/new/.
    # It connects to the risk_assessment_create view, where the suitability or risk assessment form is processed.
    # The name "risk_create" lets me link to this form using {% url 'clients:risk_create' %}.
]
# Overall, this file acts like a map between browser URLs, Django view functions, and template URL names.