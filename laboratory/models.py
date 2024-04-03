from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Laboratory(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    image = models.ImageField(
        null=True, blank=True, upload_to="laboratory_pics", default="lab_icon.avif"
    )

    CITY_CHOICES = (
        ("MANS", "Mansoura"),
        ("NDAM", "New-Dammitta"),
        ("CAI", "Cairo"),
    )
    city = models.CharField(max_length=100, choices=CITY_CHOICES, null=True, blank=True)

    rate = models.IntegerField(
        null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    phone_num = models.CharField(max_length=13)
    technology = models.CharField(max_length=50)
    about = models.TextField()
    patient = models.PositiveIntegerField()
