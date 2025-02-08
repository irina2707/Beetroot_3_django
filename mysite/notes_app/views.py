from django.shortcuts import render

def index(request):
    # Тестові дані
    notes = [
        {"title": "Перша нотатка", "content": "Це перша тестова нотатка"},
        {"title": "Друга нотатка", "content": "Це друга тестова нотатка"},
        {"title": "Третя нотатка", "content": "Це третя тестова нотатка"},
    ]
    
    return render(request, "notes_app/index.html", {"notes": notes})
