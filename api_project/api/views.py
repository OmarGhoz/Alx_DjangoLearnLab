from rest_framework.generics import ListAPIView
from rest_framework import generics , viewsets
from .models import Book
from .serializers import BookSerializer
from rest_framework.viewsets import ModelViewSet  # Ensure this is correctly imported

# List view for books
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
# CRUD operations for books
class BookViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for handling CRUD operations for the Book model.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
