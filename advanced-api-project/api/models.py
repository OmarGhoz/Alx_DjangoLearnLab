# Author model represents an author entity with a name field.
# Book model represents a book entity with a title, publication year, and a link to an Author.

from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=255, help_text="The author's name.")

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255, help_text="The book's title.")
    publication_year = models.IntegerField(help_text="The year the book was published.")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title
