# Generated by Django 4.2.3 on 2023-07-30 00:03

from django.db import migrations, models
import django.db.models.deletion


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