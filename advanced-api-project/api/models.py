from django.db import models
from django.utils import timezone

"""
Author model:
- Represents a book author.
- Has a single field `name` which stores the author's full name.
"""

class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


"""
Book model:
- Represents a book written by an author.
- Contains title and publication year.
- Has a foreign key linking each book to an Author.
"""

class Book(models.Model):
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return self.title