# Using ListAPIView for BookList
from rest_framework.generics import ListAPIView

from rest_framework.generics import ListAPIView
from .models import Book
from .serializers import BookSerializer

class BookList(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
print("BookList view successfully loaded")
