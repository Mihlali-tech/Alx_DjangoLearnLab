``markdown
# Update a Book instance

```python
from bookshelf.models import Book

# Retrieve the book and update its title
book = Book.objects.get(id=1)
book.title = "Nineteen Eighty-Four"
book.save()
print(book)

# Expected Output:
# Nineteen Eighty-Four by George Orwell (1949)