"""
API Authentication: TokenAuthentication enabled.
All endpoints require the user to provide a valid token.

Get token:
POST /api-token-auth/ with username + password
"""

from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()CRI
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]