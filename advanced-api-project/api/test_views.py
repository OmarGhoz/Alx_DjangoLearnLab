from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Book, Author

class BookAPITestCase(APITestCase):

    def setUp(self):
        # Create an author
        self.author = Author.objects.create(name="Test Author")
        # Create a book
        self.book = Book.objects.create(
            title="Test Book",
            publication_year=2020,
            author=self.author
        )
        # Define URLs
        self.list_url = reverse('book-list')  # Update with the actual name of your URL
        self.detail_url = reverse('book-detail', kwargs={'pk': self.book.id})
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Log in the test user
        self.client.login(username='testuser', password='testpassword')

        # Create an author
        self.author = Author.objects.create(name="Test Author")
        # Create a book
        self.book = Book.objects.create(
            title="Test Book",
            publication_year=2020,
            author=self.author
        )
        # Define URLs
        self.list_url = reverse('book-list')  # Update with the actual name of your URL
        self.detail_url = reverse('book-detail', kwargs={'pk': self.book.id})

    def test_list_books(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_book(self):
        data = {
            "title": "New Book",
            "publication_year": 2023,
            "author": self.author.id
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_update_book(self):
        data = {
            "title": "Updated Book",
            "publication_year": 2021,
            "author": self.author.id
        }
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Book")

    def test_delete_book(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_filter_books_by_author(self):
        response = self.client.get(self.list_url, {'author': self.author.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_books(self):
        response = self.client.get(self.list_url, {'search': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_order_books_by_publication_year(self):
        response = self.client.get(self.list_url, {'ordering': 'publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
