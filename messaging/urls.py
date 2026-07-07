from django.urls import path
from . import views

app_name = "messaging"

urlpatterns = [
    path("", views.inbox, name="inbox"),
    path("sent/", views.sent, name="sent"),
    path("archived/", views.archived, name="archived"),
    path("compose/", views.compose, name="compose"),
    path("<int:pk>/", views.detail, name="detail"),
    path("<int:pk>/archive/", views.archive_message, name="archive"),
]
