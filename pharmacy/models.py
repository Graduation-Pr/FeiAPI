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


    def __str__(self):
        return self.name


class MedCategory(models.TextChoices):
    MEDICATIONS = "Medications"
    VITAMINS = "Vitamins&supplement"


class DevSubCategory(models.TextChoices):
    # Subcategories for Home Health Care
    DIABETES_CARE = "Diabetes Care", "Diabetes Care"
    BLOOD_PRESSURE_MONITOR = "Blood Pressure Monitor", "Blood Pressure Monitor"
    THERMOMETERS = "Thermometers", "Thermometers"


class Subcategory(models.TextChoices):
    # Subcategories for Medications
    PAINKILLERS = "Painkillers", "Painkillers"
    CLOT_MEDICATIONS = "Clot-medications", "Clot-medications"
    BRONCHODILATORS = "Bronchodilators", "Bronchodilators"

    # Subcategories for Vitamins & Supplements
    VITAMIN_A = "Vitamin A", "Vitamin A"
    VITAMIN_C = "Vitamin C", "Vitamin C"
    VITAMIN_D = "Vitamin D", "Vitamin D"


class Product(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    image = models.ImageField(
        null=True, blank=True, upload_to="product_pics", default="products.jpg"
    )
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    description = models.TextField(max_length=100, default="", blank=False)
    stock = models.IntegerField(default=0)
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, related_name='product_pharmacy')

    def __str__(self):
        return self.name


class Medicine(Product):
    pill_dosage = models.CharField(max_length=10)
    category = models.CharField(max_length=40, choices=MedCategory.choices)

    subcategory = models.CharField(
        max_length=40, choices=Subcategory.choices, null=True, blank=True
    )


class Device(Product):
    category = models.CharField(max_length=50, default="Home Health Care")
    subcategory = models.CharField(
        max_length=40, choices=DevSubCategory.choices, null=True, blank=True
    )


class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_cart")
    created = models.DateTimeField(auto_now_add=True)


class CartItems(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="items", blank=True, null=True
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()



class FavProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,  on_delete=models.CASCADE)
