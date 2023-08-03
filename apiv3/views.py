from django.contrib.auth.models import User
from django.db import transaction
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import permissions, generics
from rest_framework import viewsets, views
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from apiv3.models import Book, Order, MonoSettings
from apiv3.mono import create_order, verify_signature
from apiv3.serializers import (
    BookSerializer,
    OrderSerializer,
    OrderModelSerializer,
    MonoCallbackSerializer,
    CustomTokenObtainPairSerializer,
    UserRegistrationSerializer,
)


class UrlsDetail(APIView):
    description = "List of all available endpoints"

    @method_decorator(cache_page(60 * 15))
    def get(self, request):
        data = Response(
            [
                {"disclaimer": "This is the list of all available endpoints"},
                {
                    "books": [
                        {
                            "list": "/api_v3/books/",
                            "method": "GET",
                        },
                        {
                            "create": "/api_v3/books/",
                            "method": "POST",
                        },
                        {
                            "detailed": "/api_v3/books/<int:pk>/",
                            "method": "GET",
                        },
                        {
                            "update": "/api_v3/books/<int:pk>/",
                            "method": "PUT",
                        },
                        {
                            "delete": "/api_v3/books/<int:pk>/",
                            "method": "DELETE",
                        },
                    ],
                    "users": {
                        "register": reverse("user_register"),
                        "login": reverse("user_get_token"),
                    },
                    "mono": {
                        "create_order": reverse("order"),
                        "callback": reverse("mono_callback"),
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
                "Warning": "Email and username must be unique! If you are registered, you can login: "
                "/api_v3/users/login",
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
                "Warning": "If you are not registered, please, head to /api_v3/users/register/",
            },
        ]
        return Response(data)


class BooksViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by("id")
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class OrdersViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Order.objects.all().order_by("id")
    serializer_class = OrderModelSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = LimitOffsetPagination
    filterset_fields = {"id": ["gte", "lte"]}


class OrderView(views.APIView):
    permission_classes = [permissions.AllowAny]

    @transaction.atomic
    def post(self, request):
        order = OrderSerializer(data=request.data)

        order.is_valid(raise_exception=True)

        webhook_url = request.build_absolute_uri(reverse("mono_callback"))
        order_data = create_order(order.validated_data["order"], webhook_url)

        return Response(order_data)


class OrderCallbackView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        public_key = MonoSettings.get_token()

        if not verify_signature(
            public_key, request.headers.get("X-Sign"), request.body
        ):
            return Response({"status": "signature mismatch"}, status=400)

        callback = MonoCallbackSerializer(data=request.data)
        callback.is_valid(raise_exception=True)

        try:
            order = Order.objects.get(id=callback.validated_data["reference"])
        except Order.DoesNotExist:
            return Response({"status": "order not found"}, status=404)

        if order.invoice_id != callback.validated_data["invoiceId"]:
            return Response({"status": "invoiceId mismatch"}, status=400)
        order.status = callback.validated_data["status"]
        order.save()

        return Response({"status": "ok"})
