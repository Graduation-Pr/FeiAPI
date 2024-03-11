# Generated by Django 5.0.2 on 2024-03-09 16:08

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pharmacy", "0006_alter_product_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pharmacy",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                primary_key=True,
                serialize=False,
                unique=True,
            ),
        ),
    ]