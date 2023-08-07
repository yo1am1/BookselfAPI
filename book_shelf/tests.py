import json

from django.test import TestCase, Client
from django.urls import reverse

from .models import Author, Book


class BookViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.author = Author.objects.create(name="Author Name")
        self.book = Book.objects.create(
            title="Book Title", publish_year=2022, author=self.author, genre="Fiction"
        )

    def test_get_single_book(self):
        response = self.client.get(
            reverse("book_detail_or_remove", args=[self.book.id])
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data[0]["fields"]["title"], self.book.title)
        self.assertEqual(data[0]["fields"]["publish_year"], self.book.publish_year)
        self.assertEqual(data[0]["fields"]["genre"], self.book.genre)

    def test_get_nonexistent_book(self):
        response = self.client.get(reverse("book_detail_or_remove", args=[999]))
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.content)
        self.assertEqual(data["Error"], "Book does not exist")

    def test_get_books_with_filters(self):
        response = self.client.get(reverse("books_info_or_add"), {"title": "Title"})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data), 1)

    def test_post_valid_book(self):
        new_book = {
            "title": "New Book",
            "publish_year": 2023,
            "author": "New Author",
            "genre": "Mystery",
        }
        response = self.client.post(
            reverse("books_info_or_add"),
            json.dumps(new_book),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content)
        self.assertEqual(data["title"], new_book["title"])
        self.assertEqual(data["publish_year"], new_book["publish_year"])
        self.assertEqual(data["author"], new_book["author"])
        self.assertEqual(data["genre"], new_book["genre"])

    def test_put_existing_book(self):
        updated_data = {
            "title": "Book Title",
            "publish_year": 2023,
            "author": "Updated Author",
            "genre": "Updated Genre",
        }
        response = self.client.put(
            reverse("book_detail_or_remove", args=[self.book.id]),
            json.dumps(updated_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["message"], f"Book '{self.book}' has been updated")
        self.assertEqual(data["status"], 200)

    def test_put_nonexistent_book(self):
        updated_data = {
            "title": "Updated Title",
            "publish_year": 2023,
            "author": "Updated Author",
            "genre": "Updated Genre",
        }
        response = self.client.put(
            reverse("book_detail_or_remove", args=[999]),
            json.dumps(updated_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(data["Error"], "Book does not exist")

    def test_delete_existing_book(self):
        response = self.client.delete(
            reverse("book_detail_or_remove", args=[self.book.id])
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["book"], f"'{self.book}' has been deleted")
        self.assertEqual(data["status"], 200)

    def test_delete_nonexistent_book(self):
        response = self.client.delete(reverse("book_detail_or_remove", args=[999]))
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEqual(data["Error"], "Book does not exist")

    def tearDown(self):
        self.book.delete()
        self.author.delete()
