import os

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from apiv2.models import Author, Book


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(username="testuser", password="testpassword")


@pytest.fixture
def author():
    return Author.objects.create(name="Author Name")


@pytest.fixture
def book(author):
    return Book.objects.create(title="Book Title", author=author)


@pytest.mark.django_db
def test_urls_detail(api_client):
    url = reverse("urls")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_user_registration(api_client):
    url = reverse("user_register")
    data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "newpassword12345",
    }
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_custom_token_obtain_pair(api_client, user):
    url = reverse("user_get_token")
    data = {"username": user.username, "password": "testpassword"}
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_author_list(api_client, author):
    url = reverse("author_display")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_author_detail(api_client, author):
    url = reverse("author_detailed", args=[author.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_book_list(api_client, book):
    url = reverse("book_display")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_book_detail(api_client, book):
    url = reverse("book_detailed", args=[book.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_not_authorized_book(api_client):
    url = reverse("book_create")
    data = {
        "title": "Book Title",
        "publish_year": 2023,
        "author": "Updated Author",
        "genre": "Updated Genre",
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_book_creation():
    author = Author.objects.create(name="Test Author")
    book = Book.objects.create(title="Test Book", author=author)
    assert book.id is not None
    assert str(book) == "Test Book"


if __name__ == "__main__":
    pytest.main([os.path.realpath(__file__)])
