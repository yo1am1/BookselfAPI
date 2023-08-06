from django.urls import path

from apiv3 import views
from apiv3.views import (
    OrderView,
    OrderCallbackView,
    OrdersViewSet,
    UrlsDetail,
    OrderDetailedView,
)

urlpatterns = [
    path("", UrlsDetail.as_view(), name="urls-detail"),
    path("books/", views.BookList.as_view(), name="book-list"),
    path("books/<int:pk>/", views.BookDetail.as_view(), name="book-detail"),
    path("books/create/", views.BookCreate.as_view(), name="book-create"),
    path("books/update/<int:pk>/", views.BookUpdate.as_view(), name="book-update"),
    path("books/delete/<int:pk>/", views.BookDelete.as_view(), name="book-delete"),
    path("authors/create/", views.AuthorCreate.as_view(), name="authors-create"),
    path("authors/", views.AuthorList.as_view(), name="author-list"),
    path("authors/<int:pk>/", views.AuthorDetail.as_view(), name="author-detail"),
    path(
        "authors/update/<int:pk>/", views.AuthorUpdate.as_view(), name="author-update"
    ),
    path(
        "authors/delete/<int:pk>/", views.AuthorDelete.as_view(), name="author-delete"
    ),
    path("users/register/", views.UserRegistrationView.as_view(), name="user-register"),
    path(
        "users/login/",
        views.CustomTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path("order/", OrderView.as_view(), name="order"),
    path("order/<int:pk>", OrderDetailedView.as_view(), name="order-detail"),
    path("orders/", OrdersViewSet.as_view({"get": "list"}), name="orders-list"),
    path("monobank/callback", OrderCallbackView.as_view(), name="mono_callback"),
]
