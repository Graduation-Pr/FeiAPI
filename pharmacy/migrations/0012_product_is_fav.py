# Generated by Django 5.0.2 on 2024-04-04 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pharmacy", "0011_cart_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="is_fav",
            field=models.BooleanField(default=False),
        ),
    ]