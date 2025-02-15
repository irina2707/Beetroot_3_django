from django.urls import path
from . import views

app_name = "notes_app"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:note_id>/", views.detail, name="detail"),
    path("new/", views.create, name="create"),
    path("<int:note_id>/delete/", views.delete, name="delete"),
]

