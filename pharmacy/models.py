import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User
class Pharmacy(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    image = models.ImageField(null=True, blank=True, upload_to="profile_pics", default="")
    
    CITY_CHOICES = (
        ("MANS", "Mansoura"),
        ("NDAM", "New-Dammitta"),
        ("CAI", "Cairo"),
    )
    city = models.CharField(max_length=100, choices=CITY_CHOICES, null=True, blank=True)
    
    rating = models.IntegerField(
        null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )



class Category(models.Model):
    title = models.CharField(max_length=55)

    #MEDICATIONS = 'Medications'
    #VITAMINS = 'Vitamins&supplement'
    #HOME_HEALTH_CARE = 'Home Health Care'



class Product(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    image = models.ImageField(null=True, blank=True, upload_to="profile_pics", default="")
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    description = models.TextField(max_length=100, default="", blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    #category = models.CharField(max_length=40, choices=Category.choices)
    stock = models.IntegerField(default=0)
    

    def __str__(self):
        return self.name





