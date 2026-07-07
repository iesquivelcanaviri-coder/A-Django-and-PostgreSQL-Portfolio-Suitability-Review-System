from django.urls import path
from . import views

app_name = "clients"

urlpatterns = [
    path("", views.client_list, name="list"),
    path("new/", views.client_create, name="create"),
    path("<int:pk>/", views.client_detail, name="detail"),
    path("<int:pk>/edit/", views.client_update, name="update"),
    path("<int:client_pk>/financial/", views.financial_profile_edit, name="financial"),
    path("risk/new/", views.risk_assessment_create, name="risk_create"),
]
