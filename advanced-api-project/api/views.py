from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics, permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

# ------------------- BOOK VIEWS -------------------

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    filter_backends = filter_backends
    filterset_fields = ['title', 'author', 'publication_year']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']

class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]

class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication] 

    def perform_create(self, serializer):
        serializer.save()

class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication] 

class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication] 

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = filter_backends
    filterset_fields = ['title', 'author', 'publication_year']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year']

# ------------------- AUTHOR VIEWS -------------------

class AuthorListView(generics.ListAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [AllowAny]

class AuthorDetailView(generics.RetrieveAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [AllowAny]

class AuthorCreateView(generics.CreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication] 

class AuthorUpdateView(generics.UpdateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication] 

class AuthorDeleteView(generics.DestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication] 

# ------------------- BOOK API TESTS -------------------

class BookAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="apiuser", password="Pass@1234")
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.auth_header = {"HTTP_AUTHORIZATION": f"Bearer {self.token}"}

        self.book1 = Book.objects.create(title="Test Driven Development", author=Author.objects.create(name="Kent"), publication_year=2000)
        self.book2 = Book.objects.create(title="Django APIs", author=Author.objects.create(name="Tom"), publication_year=2022)

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
        data = {"title": "New API Book", "author": self.book1.author.id, "publication_year": 2023}
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
        data = {"title": "Blocked Book", "author": self.book1.author.id, "publication_year": 2025}
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
        response = self.client.get(reverse("book-list"), {"author": self.book2.author.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_books(self):
        response = self.client.get(reverse("book-list"), {"search": "django"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_books(self):
        response = self.client.get(reverse("book-list"), {"ordering": "-publication_year"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
