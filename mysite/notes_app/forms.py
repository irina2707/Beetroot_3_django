from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    reminder = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}), 
        required=False
    )

    class Meta:
        model = Note
        fields = ["title", "text", "reminder", "category"]
