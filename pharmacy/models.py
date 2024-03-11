import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import User


class Pharmacy(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    image = models.ImageField(
        null=True, blank=True, upload_to="pharmacy_pics", default="pharmacy_icon.png"
    )

    CITY_CHOICES = (
        ("MANS", "Mansoura"),
        ("NDAM", "New-Dammitta"),
        ("CAI", "Cairo"),
    )
    city = models.CharField(max_length=100, choices=CITY_CHOICES, null=True, blank=True)

    rating = models.IntegerField(
        null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    # id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)


class Category(models.TextChoices):
    MEDICATIONS = "Medications"
    VITAMINS = "Vitamins&supplement"
    HOME_HEALTH_CARE = "Home Health Care"


class Subcategory(models.TextChoices):
    # Subcategories for Medications
    PAINKILLERS = "Painkillers", "Painkillers"
    CLOT_MEDICATIONS = "Clot-medications", "Clot-medications"
    BRONCHODILATORS = "Bronchodilators", "Bronchodilators"

    # Subcategories for Vitamins & Supplements
    VITAMIN_A = "Vitamin A", "Vitamin A"
    VITAMIN_C = "Vitamin C", "Vitamin C"
    VITAMIN_D = "Vitamin D", "Vitamin D"

    # Subcategories for Home Health Care
    DIABETES_CARE = "Diabetes Care", "Diabetes Care"
    BLOOD_PRESSURE_MONITOR = "Blood Pressure Monitor", "Blood Pressure Monitor"
    THERMOMETERS = "Thermometers", "Thermometers"


class Product(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    image = models.ImageField(
        null=True, blank=True, upload_to="product_pics", default="medicine.png"
    )
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    description = models.TextField(max_length=100, default="", blank=False)
    category = models.CharField(max_length=40, choices=Category.choices)
    subcategory = models.CharField(
        max_length=40, choices=Subcategory.choices, null=True, blank=True
    )
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)


class CartItems(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="items", blank=True, null=True
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
