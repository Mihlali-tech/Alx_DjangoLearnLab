```markdown
# Delete a Book instance

```python
from bookshelf.models import Book

# Retrieve the book and delete it
book = Book.objects.get(id=1)
book.delete()

# Verify deletion by retrieving all books
Book.objects.all()

# Expected Output:
# <QuerySet []>