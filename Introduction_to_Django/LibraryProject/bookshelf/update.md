# Update the Title of a Book Instance

## Command
```python
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()  # Save the updated title
