# notes_app/api_urls.py
from django.urls import path
from .views import NoteListCreateView, NoteRetrieveUpdateDeleteView

app_name = "notes_api"

urlpatterns = [
    path("notes/", NoteListCreateView.as_view(), name="api_notes_list_create"),
    path("notes/<int:pk>/", NoteRetrieveUpdateDeleteView.as_view(), name="api_notes_detail"),
]
