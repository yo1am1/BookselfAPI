from django.urls import path

from apiv3 import views
from apiv3.views import (
    UrlsDetail,
    CustomTokenObtainPairView,
    OrdersViewSet,
    OrderCallbackView,
    OrderView,
    UserRegistrationView,
)

# Wire up our API using automatic URL routing.
urlpatterns = [
    path("", views.UrlsDetail.as_view(), name="urls"),
    path("books/", views.BookList.as_view(), name="book_display"),
    path("books/create/", views.BookCreate.as_view(), name="book_create"),
    path("books/<int:pk>/", views.BookDetail.as_view(), name="book_detailed"),
    path("books/update/<int:pk>/", views.BookUpdate.as_view(), name="book_update"),
    path("books/delete/<int:pk>/", views.BookDelete.as_view(), name="book_delete"),
    path("authors/", views.AuthorList.as_view(), name="author_display"),
    path("authors/create/", views.AuthorCreate.as_view(), name="authors_create"),
    path("authors/<int:pk>/", views.AuthorDetail.as_view(), name="author_detailed"),
    path(
        "authors/update/<int:pk>/", views.AuthorUpdate.as_view(), name="author_update"
    ),
    path(
        "authors/delete/<int:pk>/", views.AuthorDelete.as_view(), name="author_delete"
    ),
    path("users/register/", views.UserRegistrationView.as_view(), name="user_register"),
    path(
        "users/login/",
        views.CustomTokenObtainPairView.as_view(),
        name="user_get_token",
    ),
    path("urls/", UrlsDetail.as_view(), name="urls"),
    path("orders/list/", OrdersViewSet.as_view({"get": "list"}), name="orders_list"),
    path("monobank/callback", OrderCallbackView.as_view(), name="mono_callback"),
    path("orders/", OrderView.as_view(), name="order_create"),
    path("register/", UserRegistrationView.as_view(), name="user_register"),
    path(
        "login/",
        CustomTokenObtainPairView.as_view(),
        name="user_get_token",
    ),
]
