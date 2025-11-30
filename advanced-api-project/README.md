📘 Advanced API Project – Custom Serializers & Generic Views

This project is part of the ALX Django REST Framework Learning Series, focusing on building advanced APIs using Django REST Framework (DRF). It demonstrates how to work with nested serializers, custom validation, and generic views.

🚀 Features Implemented
Models

Author

Stores an author's name.

Book

Includes title, publication year, and a foreign key referencing an author.

Creates a one-to-many relationship (one author can have many books).

📦 Serializers
BookSerializer

Serializes all fields of the Book model.

Includes custom validation to prevent future publication years.

AuthorSerializer

Serializes an author and all related books using a nested BookSerializer.

Demonstrates DRF’s handling of relationships.

🔧 Views (Using Generic Views)

Implemented using DRF’s generic view classes:

BookListCreateView — list all books or create a new one

BookDetailView — retrieve a single book

BookUpdateView — update an existing book

BookDeleteView — delete a book

Permissions:

Read operations: open to everyone

Create, update, delete: restricted to authenticated users

🔗 API Endpoints
Endpoint	Method	Description
/books/	GET	List all books
/books/	POST	Create a new book (auth required)
/books/<id>/	GET	Retrieve a book
/books/<id>/update/	PUT/PATCH	Update a book (auth required)
/books/<id>/delete/	DELETE	Delete a book (auth required)
🧪 Testing

You can test the API using:

Postman

cURL

Django admin

Python shell

Test creating authors/books and ensure nested serialization works correctly


## API Testing Guide

### ✅ Testing Strategy
The API tests cover:
- CRUD endpoint functionality for the `Book` model
- Data integrity and correct HTTP status codes
- Permission enforcement using JWT authentication
- Filtering, searching, and ordering support

### 🧪 Test File Location
Tests are implemented in:
