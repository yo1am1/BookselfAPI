# Generated by Django 4.2.3 on 2023-08-06 21:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("apiv3", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="publish_year",
            field=models.PositiveIntegerField(default=2023),
            preserve_default=False,
        ),
    ]
