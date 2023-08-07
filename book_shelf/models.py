from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=100)
    publish_year = models.IntegerField(null=True)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=100, null=True, default="None")

    def __str__(self):
        return self.title
