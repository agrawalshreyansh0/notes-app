from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Note

class NoteAPITestCase(APITestCase):

    def setUp(self):
        # Create a sample note to use in tests
        self.note = Note.objects.create(title='Sample Note', description='This is a sample description')
        self.list_url = reverse('note-list-create')  # URL for listing and creating notes
        self.detail_url = reverse('note-detail', kwargs={'pk': self.note.id})  # URL for retrieving, updating, deleting

    # Test for creating a note
    def test_create_note(self):
        data = {
            'title': 'New Note',
            'description': 'This is a new note'
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.count(), 2)  # Check if a second note was created
        self.assertEqual(response.data['title'], 'New Note')

    # Test for retrieving the note list
    def test_get_notes_list(self):
        response = self.client.get(self.list_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # There should be 1 note in the list
        self.assertEqual(response.data[0]['title'], self.note.title)

    # Test for retrieving a single note
    def test_get_single_note(self):
        response = self.client.get(self.detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.note.title)

    # Test for updating a note
    def test_update_note(self):
        data = {
            'title': 'Updated Note',
            'description': 'Updated description'
        }
        response = self.client.put(self.detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.note.refresh_from_db()  # Refresh the object from the database
        self.assertEqual(self.note.title, 'Updated Note')
        self.assertEqual(self.note.description, 'Updated description')

    # Test for deleting a note
    def test_delete_note(self):
        response = self.client.delete(self.detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Note.objects.count(), 0)  # There should be no notes left
