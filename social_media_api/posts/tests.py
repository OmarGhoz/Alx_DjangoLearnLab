from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post, Comment

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.post = Post.objects.create(author=self.user, title='Test Post', content='Test Content')

    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Test Post')
