# Generated by Django 5.0.2 on 2024-03-11 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pharmacy", "0008_alter_pharmacy_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="pharmacy",
            name="image",
            field=models.ImageField(
                blank=True, default="", null=True, upload_to="pharmacy_pics"
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="image",
            field=models.ImageField(
                blank=True, default="medicine.png", null=True, upload_to="product_pics"
            ),
        ),
    ]