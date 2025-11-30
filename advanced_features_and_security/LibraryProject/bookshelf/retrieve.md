# Retrieve a Book instance

```python
from bookshelf.models import Book

# Retrieve the book we created earlier
book = Book.objects.get(id=1)
print(book)

# Expected Output:
# 1984 by George Orwell (1949)