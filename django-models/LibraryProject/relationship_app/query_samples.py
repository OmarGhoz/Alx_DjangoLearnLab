# Import the models to be used in the queries
from relationship_app.models import Author, Book, Library, Librarian

# Query 1: Retrieve all books by a specific author
def get_books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
        books = author.books.all()  # Using the related_name 'books' from the ForeignKey in Book model
        return books
    except Author.DoesNotExist:
        return f"No author found with the name {author_name}"

# Query 2: List all books in a specific library
def get_books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()  # Using the related_name 'books' from the ManyToManyField in Library model
        return books
    except Library.DoesNotExist:
        return f"No library found with the name {library_name}"

def get_books_by_author(author):
    return Book.objects.filter(author=author)

# Query 3: Retrieve the librarian for a specific library
def get_librarian_for_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        librarian = library.librarian  # Using the related_name 'librarian' from the OneToOneField in Librarian model
        return librarian
    except Library.DoesNotExist:
        return f"No library found with the name {library_name}"
    except Librarian.DoesNotExist:
        return f"No librarian assigned to the library {library_name}"
    
    

def get_librarian_for_library(library):
    return Librarian.objects.get(library=library)