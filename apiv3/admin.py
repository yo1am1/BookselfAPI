from django.contrib import admin
from .models import Author, Book, Order, OrderItem, MonoSettings


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "genre", "author", "price", "amount")
    list_filter = ("author", "genre")
    search_fields = ("title", "author__name")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "total_price", "created_at", "status")
    list_filter = ("status",)
    search_fields = ("id", "invoice_id")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "book", "order", "amount")
    list_filter = ("order__status",)
    search_fields = ("book__title", "order__id")


@admin.register(MonoSettings)
class MonoSettingsAdmin(admin.ModelAdmin):
    list_display = ("id", "public_key")


# You can register other models as well
