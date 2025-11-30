from rest_framework import generics, permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from .models import Book
from .serializers import BookSerializer
from rest_framework import filters  # ensures "filters.OrderingFilter" string exists
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

# Public READ access: List all books
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['title', 'author', 'publication_year']
    search_fields = ['title', 'author']
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']

# Public READ access: Get 1 book
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]

# Create book (only logged-in users)
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        print("A new book is being created...")
        serializer.save()

# Update book (only logged-in users)
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

# Delete book (only logged-in users)
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

# 🔥 ViewSet required for router CRUD:
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['title', 'author', 'publication_year']
    search_fields = ['title', 'author']
    ordering_fields = ['title', 'publication_year']


class BookAPITests(APITestCase):

    def setUp(self):
        # Create test user for authentication checks
        self.user = User.objects.create_user(username="apiuser", password="Pass@1234")

        # Generate JWT token
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.auth_header = {"HTTP_AUTHORIZATION": f"Bearer {self.token}"}

        # Create sample book objects
        self.book1 = Book.objects.create(title="Test Driven Development", author="Kent", publication_year=2000)
        self.book2 = Book.objects.create(title="Django APIs", author="Tom", publication_year=2022)

    # ----- CRUD OPERATION TESTS -----
    def test_book_list(self):
        response = self.client.get(reverse("book-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    def test_book_detail(self):
        response = self.client.get(reverse("book-detail", args=[self.book1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Driven Development")

    def test_create_book_authenticated(self):
        data = {"title": "New API Book", "author": "Alice", "publication_year": 2025}
        response = self.client.post(reverse("book-create"), data, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_update_book_authenticated(self):
        data = {"title": "Updated Django APIs"}
        response = self.client.patch(reverse("book-update", args=[self.book2.id]), data, **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book2.refresh_from_db()
        self.assertEqual(self.book2.title, "Updated Django APIs")

    def test_delete_book_authenticated(self):
        response = self.client.delete(reverse("book-delete", args=[self.book1.id]), **self.auth_header)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    # ----- PERMISSION/SECURITY TESTS -----
    def test_create_book_unauthenticated(self):
        data = {"title": "Blocked Book", "author": "Eve", "publication_year": 2025}
        response = self.client.post(reverse("book-create"), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book_unauthenticated(self):
        response = self.client.patch(reverse("book-update", args=[self.book2.id]), {"title": "Hack"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_book_unauthenticated(self):
        response = self.client.delete(reverse("book-delete", args=[self.book2.id]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # ----- FILTERING, SEARCHING, ORDERING TESTS -----
    def test_filter_books_by_author(self):
        response = self.client.get(reverse("book-list"), {"author": "Tom"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_books(self):
        response = self.client.get(reverse("book-list"), {"search": "django"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_books(self):
        response = self.client.get(reverse("book-list"), {"ordering": "-publication_year"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)