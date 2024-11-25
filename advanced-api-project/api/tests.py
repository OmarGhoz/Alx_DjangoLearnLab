from django.test import TestCase
from django.urls import reverse, resolve
from api.views import BookUpdateView, BookDeleteView

class URLConfigTest(TestCase):
    def test_update_url(self):
        url = reverse('book-update', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, BookUpdateView)

    def test_delete_url(self):
        url = reverse('book-delete', kwargs={'pk': 1})
        self.assertEqual(resolve(url).func.view_class, BookDeleteView)

