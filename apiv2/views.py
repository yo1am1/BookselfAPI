from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from apiv2.models import Author, Book
from apiv2.permissions import IsAuthenticatedOrReadOnly
from apiv2.serializers import (
    AuthorSerializer,
    BookSerializer,
    UserRegistrationSerializer,
    CustomTokenObtainPairSerializer,
)


class UrlsDetail(APIView):
    description = "List of all available endpoints"

    @method_decorator(cache_page(60 * 15))
    def get(self, request):
        data = Response(
            [
                {"disclaimer": "This is the list of all available endpoints"},
                {
                    "authors": {
                        "list": reverse("author_display"),
                        "create": reverse("authors_create"),
                        "detailed": reverse("author_detailed", args=[1]),
                        "update": reverse("author_update", args=[1]),
                        "delete": reverse("author_delete", args=[1]),
                    },
                    "books": {
                        "list": reverse("book_display"),
                        "create": reverse("book_create"),
                        "detailed": reverse("book_detailed", args=[1]),
                        "update": reverse("book_update", args=[1]),
                        "delete": reverse("book_delete", args=[1]),
                    },
                    "users": {
                        "register": reverse("user_register"),
                        "login": reverse("user_get_token"),
                    },
                },
            ]
        )
        return data


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    description = "Create a new user"
    serializer_class = UserRegistrationSerializer

    def get(self, request):
        data = [
            {
                "username": "test",
                "email": "test@test.com",
                "password": "test1234",
            },
            {
                "Warning": f"Email and username must be unique! If you are registered, you can login: {reverse('user_register')}",
            },
        ]

        return Response(data)


class CustomTokenObtainPairView(TokenObtainPairView):
    queryset = User.objects.all()
    description = "Get token"
    serializer_class = CustomTokenObtainPairSerializer

    def get(self, request):
        data = [
            {"text": "Please, enter your username and password"},
            {
                "Warning": f"If you are not registered, please, head to {reverse('user_register')}",
            },
        ]
        return Response(data)


class AuthorList(generics.ListAPIView):
    queryset = Author.objects.all()
    description = "List of authors"
    serializer_class = AuthorSerializer

    @method_decorator(cache_page(60 * 15))
    def get(self, request):
        queryset = Author.objects.all()
        name = self.request.query_params.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class AuthorCreate(generics.CreateAPIView):
    queryset = Author.objects.all()
    description = "Create a new author"
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class AuthorDetail(generics.RetrieveAPIView):
    queryset = Author.objects.all()
    description = "Retrieve an author"
    serializer_class = AuthorSerializer


class AuthorUpdate(generics.UpdateAPIView):
    queryset = Author.objects.all()
    description = "Update an author"
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class AuthorDelete(generics.DestroyAPIView):
    queryset = Author.objects.all()
    description = "Delete an author"
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    description = "List of all books"
    serializer_class = BookSerializer

    @method_decorator(cache_page(60 * 15))
    def get(self, request):
        queryset = Book.objects.all()
        title = self.request.query_params.get("title")
        author = self.request.query_params.get("author")
        genre = self.request.query_params.get("genre")

        if title:
            queryset = queryset.filter(title__icontains=title)
        if author:
            queryset = queryset.filter(author__name__icontains=author)
        if genre:
            queryset = queryset.filter(genre__icontains=genre)

        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class BookDetail(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    description = "Retrieve a book"
    serializer_class = BookSerializer


class BookCreate(generics.CreateAPIView):
    queryset = Book.objects.all()
    description = "Create a new book"
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookUpdate(generics.UpdateAPIView):
    queryset = Book.objects.all()
    description = "Update a book"
    serializer_class = BookSerializer
    lookup_url_kwarg = "pk"
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookDelete(generics.DestroyAPIView):
    description = "Delete a book"
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_url_kwarg = "pk"
    permission_classes = [IsAuthenticatedOrReadOnly]
