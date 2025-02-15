
from django.shortcuts import render, get_object_or_404, redirect
from .models import Note
from .forms import NoteForm
from rest_framework import generics
from .serializers import NoteSerializer

# Головна сторінка з нотатками
def index(request):
    query = request.GET.get("q")  # Отримуємо параметр пошуку з URL
    notes = Note.objects.all().order_by("-reminder")

    if query:
        notes = notes.filter(title__icontains=query)  # Фільтр за заголовком (незалежно від регістру)

    return render(request, "notes_app/index.html", {"notes": notes, "query": query})

# Деталі нотатки + редагування
def detail(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    
    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect("notes_app:index")
    else:
        form = NoteForm(instance=note)
    
    return render(request, "notes_app/detail.html", {"note": note, "form": form})

# Створення нової нотатки
def create(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("notes_app:index")
    else:
        form = NoteForm()
    
    return render(request, "notes_app/form.html", {"form": form})

# Видалення нотатки
def delete(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    
    if request.method == "POST":
        note.delete()
        return redirect("notes_app:index")
    
    return render(request, "notes_app/delete.html", {"note": note})


# API для перегляду всіх нотаток та створення нової
class NoteListCreateView(generics.ListCreateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

# API для перегляду, редагування та видалення конкретної нотатки
class NoteRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer