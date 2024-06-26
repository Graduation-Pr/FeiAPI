from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from accounts.models import User
import uuid


# Pharmacy Model
class Pharmacy(models.Model):
    # Pharmacy name with max length of 50 characters
    name = models.CharField(max_length=50, null=False, blank=False)

    # Pharmacy image with default and optional upload settings
    image = models.ImageField(
        null=True, blank=True, upload_to="pharmacy_pics", default="pharmacy_icon.png"
    )

    # Choices for city field
    CITY_CHOICES = (
        ("MANS", "Mansoura"),
        ("NDAM", "New-Dammitta"),
        ("CAI", "Cairo"),
    )
    # City field with choices
    city = models.CharField(max_length=100, choices=CITY_CHOICES, null=True, blank=True)

    # Rating field with validators for minimum and maximum values
    rating = models.IntegerField(
        null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    def __str__(self):
        return self.name

# Medication Category Choices
class MedCategory(models.TextChoices):
    MEDICATIONS = "Medications"
    VITAMINS = "Vitamins&supplement"

# Device Subcategory Choices for Home Health Care
class DevSubCategory(models.TextChoices):
    DIABETES_CARE = "Diabetes Care", "Diabetes Care"
    BLOOD_PRESSURE_MONITOR = "Blood Pressure Monitor", "Blood Pressure Monitor"
    THERMOMETERS = "Thermometers", "Thermometers"

# Subcategory Choices for different products
class Subcategory(models.TextChoices):
    PAINKILLERS = "Painkillers", "Painkillers"
    CLOT_MEDICATIONS = "Clot-medications", "Clot-medications"
    BRONCHODILATORS = "Bronchodilators", "Bronchodilators"
    VITAMIN_A = "Vitamin A", "Vitamin A"
    VITAMIN_C = "Vitamin C", "Vitamin C"
    VITAMIN_D = "Vitamin D", "Vitamin D"

# Product Model
class Product(models.Model):
    # Product name with max length of 100 characters
    name = models.CharField(max_length=100, null=False, blank=False)

    # Product image with default and optional upload settings
    image = models.ImageField(
        null=True, blank=True, upload_to="product_pics", default="products.jpg"
    )

    # Product price with max digits and decimal places
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0)

    # Product description with max length of 100 characters
    description = models.TextField(max_length=100, default="", blank=False)

    # Stock quantity of the product
    stock = models.IntegerField(default=0)

    # Foreign key relationship with Pharmacy
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, related_name='product_pharmacy')

    def __str__(self):
        return self.name

# Medicine Model inheriting from Product
class Medicine(Product):
    # Dosage information for the medicine
    pill_dosage = models.CharField(max_length=10)

    # Category of the medicine with choices from MedCategory
    category = models.CharField(max_length=40, choices=MedCategory.choices)

    # Subcategory of the medicine with choices from Subcategory
    subcategory = models.CharField(
        max_length=40, choices=Subcategory.choices, null=True, blank=True
    )

# Device Model inheriting from Product
class Device(Product):
    # Default category for devices
    category = models.CharField(max_length=50, default="Home Health Care")

    # Subcategory of the device with choices from DevSubCategory
    subcategory = models.CharField(
        max_length=40, choices=DevSubCategory.choices, null=True, blank=True
    )

# Cart Model
class Cart(models.Model):
    # UUID for the cart
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)

    # One-to-one relationship with User
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_cart")

    # Auto timestamp for cart creation
    created = models.DateTimeField(auto_now_add=True)

# CartItems Model
class CartItems(models.Model):
    # Foreign key relationship with Cart
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="items", blank=True, null=True
    )

    # Foreign key relationship with Product
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    # Quantity of the product in the cart
    quantity = models.PositiveIntegerField()

# FavProduct Model
class FavProduct(models.Model):
    # Foreign key relationship with User
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Foreign key relationship with Product
    product = models.ForeignKey(Product, on_delete=models.CASCADE)