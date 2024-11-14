from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # Display these fields in the list view
    search_fields = ('title', 'author')  # Add search functionality for these fields
    list_filter = ('publication_year',)  # Filter by publication year

admin.site.register(Book, BookAdmin)

"admin.ModelAdmin"

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser  # Import the CustomUser model

class CustomUserAdmin(UserAdmin):
    # Extend the UserAdmin to display custom fields
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo')}),
    )  # Adds date_of_birth and profile_photo to the admin form

# Register the CustomUser model with the CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)
