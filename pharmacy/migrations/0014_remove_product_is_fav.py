# Generated by Django 5.0.2 on 2024-06-21 14:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("pharmacy", "0013_favproduct"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="is_fav",
        ),
    ]