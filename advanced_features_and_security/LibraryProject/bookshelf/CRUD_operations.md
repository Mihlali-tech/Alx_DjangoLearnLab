# Django ORM CRUD Operations

## Create

```python
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print(book)
# Output: 1984 by George Orwell (1949)
```

## Retrieve

```python
books = Book.objects.all()
print(books)
# Output: <QuerySet [<Book: 1984 by George Orwell (1949)>]>
```

## Update

```python
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
print(book)
# Output: Nineteen Eighty-Four by George Orwell (1949)
```

## Delete

```python
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
print(Book.objects.all())
# Output: <QuerySet []>
```