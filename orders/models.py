# django imports
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.conf import settings
from django.db import models
# internal imports
from pharmacy.models import Product
from accounts.models import User


class CreditCard(models.Model):
    """
    Model to store credit card information.
    """
    # Constants for card types
    MASTER_CARD = "MasterCard"
    VISA = "VISA"
    AMERICAN_EXPRESS = "American Express"

    # Choices for card types
    CARD_TYPE_CHOICES = [
        (MASTER_CARD, "MasterCard"),
        (VISA, "Visa"),
        (AMERICAN_EXPRESS, "American Express"),
    ]

    # Fields for CreditCard model
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.CharField(
        max_length=16, validators=[MinLengthValidator(16), MaxLengthValidator(16)]
    )
    expiration_date = models.CharField(
        max_length=5  # Consider adding validation for date format (MM/YY)
    )
    cvv = models.CharField(
        max_length=3, validators=[MinLengthValidator(3), MaxLengthValidator(3)]
    )
    card_type = models.CharField(max_length=16, choices=CARD_TYPE_CHOICES)
    card_image = models.ImageField(upload_to="card_images/", blank=True, null=True)

    def __str__(self):
        return f"Card ending with {self.card_number[-4:]} for user {self.user}"

    class Meta:
        verbose_name = "Credit Card"
        verbose_name_plural = "Credit Cards"

    def save(self, *args, **kwargs):
        """
        Override save method to set default card images based on card type.
        """
        if not self.card_image:
            if self.card_type == self.VISA:
                self.card_image.name = "card_images/v.png"
            elif self.card_type == self.MASTER_CARD:
                self.card_image.name = "card_images/ms.jpg"
            elif self.card_type == self.AMERICAN_EXPRESS:
                self.card_image.name = "card_images/am.jpeg"
        super().save(*args, **kwargs)


class Order(models.Model):
    """
    Model to store order information.
    """
    # Constants for payment status
    PAYMENT_STATUS_PENDING = "P"
    PAYMENT_STATUS_COMPLETE = "C"
    PAYMENT_STATUS_FAILED = "F"

    # Choices for payment status
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, "Pending"),
        (PAYMENT_STATUS_COMPLETE, "Complete"),
        (PAYMENT_STATUS_FAILED, "Failed"),
    ]

    # Fields for Order model
    placed_at = models.DateTimeField(auto_now_add=True)
    pending_status = models.CharField(
        max_length=50, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.pending_status

    @property
    def total_price(self):
        """
        Calculate the total price of all items in the order.
        """
        items = self.items.all()
        total = sum([item.quantity * item.product.price for item in items])
        return total


class OrderItem(models.Model):
    """
    Model to store items in an order.
    """
    # Fields for OrderItem model
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.product.name