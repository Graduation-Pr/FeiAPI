# Generated by Django 5.0.2 on 2024-03-07 18:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pharmacy", "0001_initial"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Category",
        ),
        migrations.AddField(
            model_name="product",
            name="category",
            field=models.CharField(
                choices=[
                    ("Medications", "Medications"),
                    ("Vitamins&supplement", "Vitamins"),
                    ("Home Health Care", "Home Health Care"),
                ],
                default="",
                max_length=40,
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="product",
            name="subcategory",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Painkillers", "Painkillers"),
                    ("Clot-medications", "Clot-medications"),
                    ("Bronchodilators", "Bronchodilators"),
                    ("Vitamin A", "Vitamin A"),
                    ("Vitamin C", "Vitamin C"),
                    ("Vitamin D", "Vitamin D"),
                    ("Diabetes Care", "Diabetes Care"),
                    ("Blood Pressure Monitor", "Blood Pressure Monitor"),
                    ("Thermometers", "Thermometers"),
                ],
                max_length=40,
                null=True,
            ),
        ),
    ]
