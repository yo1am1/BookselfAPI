import json

from django.core.serializers import serialize
from django.db.models import Q
from django.views import View

from .models import Book, Author

from django.http import JsonResponse, HttpResponse


def urls(request):
    return JsonResponse(
        {
            "books": {
                "list": "/api/books/",
                "filter": "/api/books/filter/ and insert json in postman",
                "detail": "/api/books/<int:book_id>",
            },
            "authors": {
                "list": "/api/authors/",
                "detail": "/api/authors/<int:author_id>",
            },
        }
    )


class BookView(View):
    def get(self, request, book_id=None):
        if book_id is not None:
            try:
                book = Book.objects.get(id=book_id)
                book_data = serialize(
                    "json",
                    [book],
                    indent=4,
                )
                return HttpResponse(book_data, content_type="application/json")
            except Book.DoesNotExist:
                return JsonResponse({"Error": "Book does not exist", "status": 404})
        else:
            title = request.GET.get("title")
            author = request.GET.get("author")
            publish_year = request.GET.get("publish_year")
            genre = request.GET.get("genre")

            filters = Q()
            if title:
                filters &= Q(title__icontains=title)
            if author:
                filters &= Q(author__icontains=author)
            if publish_year:
                filters &= Q(publish_year__icontains=publish_year)
            if genre:
                filters &= Q(genre__icontains=genre)

            books = Book.objects.filter(filters)

            if not books:
                raise Book.DoesNotExist and JsonResponse(
                    {
                        "message": "No books found",
                        "status": 404,
                    }
                )

            books_data = serialize(
                "json",
                books,
                fields=("title", "publish_year", "author", "genre"),
                indent=4,
            ).replace("\n", " ")
            return HttpResponse(books_data, content_type="application/json")

    def post(self, request):
        try:
            request_body = json.loads(request.body)
        except ValueError:
            return JsonResponse({"message": "Invalid data", "status": 400})
        title = request_body.get("title")
        publish_year = request_body.get("publish_year")
        author = request_body.get("author")
        genre = request_body.get("genre")

        if Book.objects.filter(title=title).exists():
            return JsonResponse({"message": "Book already exists", "status": 400})

        if title is None or publish_year is None or author is None or genre is None:
            return JsonResponse(
                {
                    "message": "Missing data field. Please, check your input",
                    "fields": {1: "title", 2: "publish_year", 3: "author", 4: "genre"},
                    "status": 400,
                }
            )
        author = Author.objects.get_or_create(name=author)

        book = Book.objects.create(
            title=title,
            publish_year=publish_year,
            author=author,
            genre=genre,
        )

        request_body["id"] = book.id
        return JsonResponse(request_body, status=201)

    def put(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)

            request_body = json.loads(request.body)

            updated_fields = []

            if request_body.get("title") and book.title != request_body["title"]:
                book.title = request_body["title"]
                updated_fields.append("title")
            if (
                request_body.get("publish_year")
                and book.publish_year != request_body["publish_year"]
            ):
                book.publish_year = request_body["publish_year"]
                updated_fields.append("publish_year")
            if request_body.get("author") and book.author != request_body["author"]:
                book.author = request_body["author"]
                updated_fields.append("author")
            if request_body.get("genre") and book.genre != request_body["genre"]:
                book.genre = request_body["genre"]
                updated_fields.append("genre")

            if not updated_fields:
                return JsonResponse(
                    {
                        "message": "No fields were updated",
                        "status": 200,
                    }
                )

            book.title = request_body.get("title", book.title)
            book.publish_year = request_body.get("publish_year", book.publish_year)
            book.author = request_body.get("author", book.author)
            book.genre = request_body.get("genre", book.genre)
            book.save()

            Author.objects.get_or_create(name=book.author)

            context = {
                "message": f"Book '{book}' has been updated",
                "updated_fields": updated_fields,
                "book": serialize(
                    "json",
                    [book],
                    fields=("title", "publish_year", "author", "genre"),
                    indent=4,
                ).replace("\n", ""),
                "status": 200,
            }
            return JsonResponse(context, safe=False)
        except Book.DoesNotExist:
            return JsonResponse({"Error": "Book does not exist", "status": 400})
        except ValueError:
            return JsonResponse({"message": "Invalid data", "status": 400})

    def delete(self, request, book_id):
        try:
            book = Book.objects.get(id=book_id)
            book.delete()
            context = {"book": f"'{book}' has been deleted", "status": 204}
            return JsonResponse(context, safe=False)
        except Book.DoesNotExist:
            return JsonResponse({"Error": "Book does not exist", "status": 400})


class AuthorsView(View):
    def get(self, request, author_id=None):
        if author_id is not None:
            try:
                author = Author.objects.get(id=author_id)
                author_data = serialize("json", [author], indent=4)
                return HttpResponse(author_data, content_type="application/json")
            except Author.DoesNotExist:
                return JsonResponse({"Error": "Author does not exist"}, status=404)
        else:
            name = request.GET.get("name")

            filters = Q()
            if name:
                filters &= Q(name__icontains=name)

            authors = Author.objects.filter(filters)

            if not authors:
                return JsonResponse(
                    {
                        "message": "No authors found",
                        "status": 404,
                    }
                )

            authors_data = serialize("json", authors, indent=4).replace("\n", " ")
            return HttpResponse(authors_data, content_type="application/json")
