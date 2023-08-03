from django.urls import include, path
from rest_framework import routers

from .views import (
    BooksViewSet,
    OrderView,
    OrdersViewSet,
    OrderCallbackView,
    UserRegistrationView,
    CustomTokenObtainPairView,
    UrlsDetail,
)

router = routers.DefaultRouter()
router.register(r"books", BooksViewSet, basename="books")
router.register(r"orders", OrdersViewSet, basename="orders")

# Wire up our API using automatic URL routing.
urlpatterns = [
    path("", include(router.urls)),
    path("urls/", UrlsDetail.as_view(), name="urls"),
    path("order/", OrderView.as_view(), name="order"),
    path("monobank/callback", OrderCallbackView.as_view(), name="mono_callback"),
    path("register/", UserRegistrationView.as_view(), name="user_register"),
    path(
        "login/",
        CustomTokenObtainPairView.as_view(),
        name="user_get_token",
    ),
]
