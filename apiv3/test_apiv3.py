import os

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from apiv3.models import Author, Book
from apiv3.serializers import BookSerializer


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def author():
    return Author.objects.create(name='Test Author')


@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='testpassword244685')


@pytest.fixture
def access_token(user):
    return AccessToken.for_user(user)


@pytest.fixture
def authenticated_client(api_client, access_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    return client


@pytest.fixture
def book(author):
    return Book.objects.create(
        title='Test Book',
        genre='Fiction',
        author=author,
        publish_year=2023,
        price=20,
        amount=10
    )


@pytest.mark.django_db
def test_urls_detail(api_client):
    user = User.objects.create_user(username='testuser', password='testpassword')
    token, created = Token.objects.get_or_create(user=user)

    api_client = APIClient()
    api_client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

    url = reverse('urls-detail')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert 'disclaimer' in data[0]
    assert 'authors' in data[1]
    assert 'books' in data[1]
    assert 'detailed' in data[1]['authors']
    assert 'update' in data[1]['authors']
    assert 'delete' in data[1]['authors']

    assert 'list' in data[1]['books']
    assert 'create' in data[1]['books']
    assert 'detailed' in data[1]['books']
    assert 'update' in data[1]['books']
    assert 'delete' in data[1]['books']

    assert 'register' in data[1]['users']
    assert 'login' in data[1]['users']

    assert 'order' in data[1]['mono']
    assert 'order_detailed' in data[1]['mono']
    assert 'order_list' in data[1]['mono']


@pytest.mark.django_db
def test_author_list(api_client, author):
    url = reverse('author-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0


@pytest.mark.django_db
def test_book_detail(api_client, book):
    url = reverse('book-detail', args=[book.id])
    response = api_client.get(url)
    print(response.data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == 'Test Book'
    assert response.data['author'] == 1


@pytest.mark.django_db
def test_book_create_unauthorized(api_client):
    url = reverse('book-create')
    data = {
        'title': 'New Book',
        'genre': 'Mystery',
        'author': {'name': 'New Author'},
        'publish_year': 2022,
        'price': 25,
        'amount': 5
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert not Book.objects.filter(title='New Book').exists()


@pytest.mark.django_db
def test_author_update_unauthorized(api_client, author):
    url = reverse('author-update', args=[author.id])
    data = {'name': 'Updated Author Name'}
    response = api_client.put(url, data, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert not Author.objects.get(id=author.id).name == 'Updated Author Name'


@pytest.mark.django_db
def test_book_create_authorized(authenticated_client, author):
    url = reverse('book-create')
    data = {
        'title': 'New Book',
        'genre': 'Mystery',
        'author': author.id,
        'publish_year': 2022,
        'price': 25,
        'amount': 5
    }
    response = authenticated_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Book.objects.filter(title='New Book').exists()


@pytest.mark.django_db
def test_book_update_authorized(authenticated_client, book):
    url = reverse('book-update', args=[book.id])
    data = {'title': 'Updated Book Title', 'genre': 'Mystery', 'publish_year': 2022, 'price': 25, 'amount': 5,
            'author': 1}
    response = authenticated_client.put(url, data, format='json')
    print(response.data)
    assert response.status_code == status.HTTP_200_OK
    assert Book.objects.get(id=book.id).title == 'Updated Book Title'


@pytest.mark.django_db
def test_book_delete_authorized(authenticated_client, book):
    url = reverse('book-delete', args=[book.id])
    response = authenticated_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Book.objects.filter(id=book.id).exists()


@pytest.mark.django_db
def test_author_creation():
    author = Author.objects.create(name='Test Author')
    assert author.id is not None
    assert str(author) == 'Test Author'


@pytest.mark.django_db
def test_author_remove():
    author = Author.objects.create(name='Test Author')
    author.delete()
    assert not Author.objects.filter(name='Test Author').exists()


@pytest.mark.django_db
def test_book_creation(author):
    book = Book.objects.create(
        title='Test Book',
        genre='Fiction',
        author=author,
        publish_year=2023,
        price=20,
        amount=10
    )
    assert book.id is not None
    assert str(book) == 'Test Book'


@pytest.mark.django_db
def test_book_remove(author):
    book = Book.objects.create(
        title='Test Book',
        genre='Fiction',
        author=author,
        publish_year=2023,
        price=20,
        amount=10
    )
    book.delete()
    assert not Book.objects.filter(title='Test Book').exists()


@pytest.mark.django_db
def test_book_serializer():
    author = Author.objects.create(name='Test Author')
    data = {
        'title': 'Test Book',
        'genre': 'Fiction',
        'author': author.id,
        'publish_year': 2023,
        'price': 20,
        'amount': 10
    }
    serializer = BookSerializer(data=data)
    assert serializer.is_valid()
    book = serializer.save()
    assert book.id is not None
    assert str(book) == 'Test Book'


@pytest.mark.django_db
def test_book_list_view():
    client = APIClient()
    url = reverse('book-list')
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 4


if __name__ == '__main__':
    pytest.main([os.path.realpath(__file__)])
