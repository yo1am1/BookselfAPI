from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path("", views.urls, name="urls"),
    path("books/", csrf_exempt(views.BookView.as_view()), name="books_info_or_add"),
    path("books/filter/", views.BookFilteredView.as_view(), name="books_filter"),
    path(
        "books/<int:book_id>",
        csrf_exempt(views.BookView.as_view()),
        name="book_detail_or_remove",
    ),
    path("authors/", views.AuthorsView.as_view(), name="authors_info"),
    path("authors/<int:author_id>", views.AuthorsView.as_view(), name="author_detail"),
]