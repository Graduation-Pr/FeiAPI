# Generated by Django 5.0.2 on 2024-03-11 22:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Laboratory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                (
                    "image",
                    models.ImageField(
                        blank=True, default="", null=True, upload_to="profile_pics"
                    ),
                ),
                (
                    "city",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("MANS", "Mansoura"),
                            ("NDAM", "New-Dammitta"),
                            ("CAI", "Cairo"),
                        ],
                        max_length=100,
                        null=True,
                    ),
                ),
                (
                    "rating",
                    models.IntegerField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(5),
                        ],
                    ),
                ),
                ("phone_num", models.CharField(max_length=13)),
                ("technology", models.CharField(max_length=50)),
                ("about", models.TextField()),
                ("patient", models.PositiveIntegerField()),
            ],
        ),
    ]
