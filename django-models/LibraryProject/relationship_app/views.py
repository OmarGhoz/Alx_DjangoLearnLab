from django.shortcuts import render
from django.views.generic.detail import DetailView  # Explicitly import DetailView
from django.views.generic import ListView
from .models import Library, Book

# Class-based view for displaying library details
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'  # Ensure this template exists
    context_object_name = 'library'

# Example function-based view for listing all books and their authors
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            return redirect('home')  # Redirect to a homepage or any other page you prefer
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render

# Check function to validate if the user is an admin
def is_admin(user):
    return user.userprofile.role == 'Admin'

# Check function to validate if the user is a librarian
def is_librarian(user):
    return user.userprofile.role == 'Librarian'

# Check function to validate if the user is a member
def is_member(user):
    return user.userprofile.role == 'Member'

# Admin view with access restricted to Admin users only
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

# Librarian view with access restricted to Librarian users only
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

# Member view with access restricted to Member users only
@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')

from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book

@permission_required('relationship_app.can_add_book')
def add_book(request):
    # Logic to add a book goes here
    return render(request, 'relationship_app/add_book.html')

@permission_required('relationship_app.can_change_book')
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    # Logic to edit a book goes here
    return render(request, 'relationship_app/edit_book.html', {'book': book})

@permission_required('relationship_app.can_delete_book')
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    # Logic to delete a book goes here
    book.delete()
    return redirect('relationship_app:book_list')
