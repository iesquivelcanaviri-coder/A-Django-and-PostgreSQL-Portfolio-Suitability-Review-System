from django.urls import path
from . import views

app_name = "mandates"

urlpatterns = [
    path("", views.mandate_list, name="list"),
    path("new/", views.mandate_create, name="create"),
    path("<int:pk>/", views.mandate_detail, name="detail"),
    path("<int:pk>/edit/", views.mandate_update, name="update"),
    path("<int:pk>/approve/", views.mandate_approve, name="approve"),
    path("holdings/new/", views.holding_create, name="holding_create"),
    path("holdings/<int:pk>/delete/", views.holding_delete, name="holding_delete"),
    path("projects/", views.project_list, name="projects"),
    path("projects/new/", views.project_create, name="project_create"),
]
