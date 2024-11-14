from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Document
from .forms import DocumentForm

# View for listing all documents (requires 'can_view' permission)
@permission_required('bookshelf.can_view', raise_exception=True)
def document_list(request):
    # Secure data access through Django ORM
    documents = Document.objects.all()
    return render(request, 'document_list.html', {'documents': documents})

# View for viewing a single document (requires 'can_view' permission)
@permission_required('bookshelf.can_view', raise_exception=True)
def document_detail(request, document_id):
    # Using Django ORM to securely fetch the document by ID
    document = get_object_or_404(Document, id=document_id)
    return render(request, 'document_detail.html', {'document': document})

# View for creating a new document (requires 'can_create' permission)
@permission_required('bookshelf.can_create', raise_exception=True)
def document_create(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST)
        if form.is_valid():
            # Save the validated data to prevent SQL injection
            form.save()
            return redirect('document_list')
    else:
        form = DocumentForm()
    return render(request, 'document_form.html', {'form': form})

# View for editing an existing document (requires 'can_edit' permission)
@permission_required('bookshelf.can_edit', raise_exception=True)
def document_edit(request, document_id):
    # Fetching the document securely using ORM
    document = get_object_or_404(Document, id=document_id)
    if request.method == 'POST':
        form = DocumentForm(request.POST, instance=document)
        if form.is_valid():
            # Save the validated data to prevent SQL injection
            form.save()
            return redirect('document_detail', document_id=document.id)
    else:
        form = DocumentForm(instance=document)
    return render(request, 'document_form.html', {'form': form})

# View for deleting a document (requires 'can_delete' permission)
@permission_required('bookshelf.can_delete', raise_exception=True)
def document_delete(request, document_id):
    # Fetching the document securely using ORM
    document = get_object_or_404(Document, id=document_id)
    if request.method == 'POST':
        # Delete only on POST to prevent accidental deletions
        document.delete()
        return redirect('document_list')
    return render(request, 'document_confirm_delete.html', {'document': document})

book_list 
from .forms import ExampleForm