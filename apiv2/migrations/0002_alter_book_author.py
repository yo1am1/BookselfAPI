# Generated by Django 4.2.3 on 2023-07-30 00:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("apiv2", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="apiv2.author"
            ),
        ),
    ]
