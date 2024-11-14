from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # Display these fields in the list view
    search_fields = ('title', 'author')  # Add search functionality for these fields
    list_filter = ('publication_year',)  # Filter by publication year

admin.site.register(Book, BookAdmin)

"admin.ModelAdmin"
