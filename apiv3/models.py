import requests
from django.conf import settings
from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)


class Mono(models.Model):
    urls = models.CharField(max_length=1000)


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    amount = models.IntegerField()
    genre = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.title


class Order(models.Model):
    books = models.ManyToManyField(Book, through="OrderItem")
    total_price = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    invoice_id = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.IntegerField()


class MonoSettings(models.Model):
    public_key = models.CharField(max_length=1000)

    @classmethod
    def get_token(cls):
        try:
            return cls.objects.last().public_key
        except AttributeError:
            key = requests.get(
                "https://api.monobank.ua/api/merchant/pubkey",
                headers={"X-Token": settings.MONOBANK_API_KEY},
            ).json()["key"]
            cls.objects.create(public_key=key)
            return key
