from django.shortcuts import render
from .models import Note

def index(request):
    notes = Note.objects.all()  # Отримуємо всі нотатки з бази
    return render(request, "notes_app/index.html", {"notes": notes})
