from django.urls import path
from . import views

app_name = "updates"

urlpatterns = [
    path("", views.update_list, name="list"),
    path("new/", views.update_create, name="create"),
]


