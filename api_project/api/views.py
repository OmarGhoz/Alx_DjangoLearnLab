from rest_framework.generics import ListAPIView
from rest_framework import generics , viewsets
from .models import Book
from .serializers import BookSerializer
from rest_framework.viewsets import ModelViewSet  # Ensure this is correctly imported
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.permissions import BasePermission

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
    permission_classes = [IsAuthenticated]
    permission_classes = [IsOwnerOrReadOnly]

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read-only permissions are allowed for any request
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # Write permissions are only allowed to the owner of the object
        return obj.owner == request.user