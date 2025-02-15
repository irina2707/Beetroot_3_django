from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import Note, Category


class NoteAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.category = Category.objects.create(title="Тестова категорія")

        self.note = Note.objects.create(
            title="Тестова нотатка",
            text="Це тестовий вміст",
            category=self.category
        )

        self.notes_list_url = reverse("notes_api:api_notes_list_create")
        self.note_url = reverse("notes_api:api_notes_detail", args=[self.note.id])


    def test_get_notes_list(self):
        """Перевірка отримання списку нотаток"""
        response = self.client.get(self.notes_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Тестова нотатка")

    def test_create_note(self):
        """Перевірка створення нової нотатки через API"""
        data = {
            "title": "Нова нотатка",
            "text": "Новий вміст",
            "category": self.category.id
        }
        response = self.client.post(self.notes_list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.count(), 2)
        self.assertEqual(Note.objects.last().title, "Нова нотатка")

    def test_get_note_detail(self):
        """Перевірка отримання деталей нотатки"""
        response = self.client.get(self.note_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Тестова нотатка")

    def test_update_note(self):
        """Перевірка оновлення нотатки"""
        updated_data = {
            "title": "Оновлена нотатка",
            "text": "Оновлений вміст",
            "category": self.category.id
        }
        response = self.client.put(self.note_url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, "Оновлена нотатка")

    def test_delete_note(self):
        """Перевірка видалення нотатки"""
        response = self.client.delete(self.note_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Note.objects.count(), 0)

class NoteViewsTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title="Тестова категорія")  
        self.note = Note.objects.create(
            title="Тестова нотатка",
            text="Це тестовий вміст",
            category=self.category  
        )

    def test_index_view(self):
        """Перевірка головної сторінки з нотатками"""
        response = self.client.get(reverse("notes_app:index"))
        self.assertEqual(response.status_code, 200)  # Код відповіді має бути 200 (OK)
        self.assertContains(response, "Тестова нотатка")  # Переконуємось, що нотатка відображається на сторінці

    def test_detail_view(self):
        """Перевірка сторінки деталей нотатки"""
        response = self.client.get(reverse("notes_app:detail", args=[self.note.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Тестова нотатка")

    def test_create_note(self):
        """Перевірка створення нотатки"""
        response = self.client.post(reverse("notes_app:create"), {
            "title": "Нова нотатка",
            "text": "Вміст нотатки",
            "category": self.category.id,  
        }, follow=True)

        # Перевірка, що форма доступна у відповідному контексті
        if response.status_code == 200 and response.context and "form" in response.context:
            print(response.context["form"].errors)
        
        self.assertEqual(response.status_code, 200)  # Має бути сторінка створеної нотатки
        self.assertEqual(Note.objects.count(), 2)  # Переконуємось, що нотатка додалась в БД

    def test_delete_note(self):
        """Перевірка видалення нотатки"""
        response = self.client.post(reverse("notes_app:delete", args=[self.note.id]), follow=True)

        # Перевірка, що форма доступна у відповідному контексті
        if response.status_code == 200 and response.context and "form" in response.context:
            print(response.context["form"].errors)

        self.assertEqual(response.status_code, 200)  # Має бути сторінка після видалення
        self.assertEqual(Note.objects.count(), 0)  # Переконуємось, що нотатка видалена

    def test_search_notes(self):
        """Перевірка пошуку нотаток"""
        response = self.client.get(reverse("notes_app:index") + "?q=Тестова")
        self.assertContains(response, "Тестова нотатка")  # Має знаходитись нотатка
