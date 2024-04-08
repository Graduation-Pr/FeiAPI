from datetime import datetime
from django.db import models
from accounts.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator


# CANCEL_REASON = (
#     ("Scedual Change", "Scedual Change"),
#     ("Weather Condition", "Weather Condition"),
#     ("Unexpected Work", "Unexpected Work"),
#     ("Childcare Issue", "Childcare Issue"),
#     ("Tavel Delays", "Tavel Delays"),
#     ("Other", "Other"),
# )

SERVICES = (
    ("Standard Appointment", "Standard Appointment"),
    ("Specialist Consultations", "Specialist Consultations"),
    ("follow-up appointment", "follow-up appointment"),
)
class Service(models.Model):
    service = models.CharField(max_length=50, choices=SERVICES)
    price = models.PositiveBigIntegerField()
    
    def __str__(self):
        return f"{self.service}"

class CreditCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16, validators=[MinLengthValidator(16), MaxLengthValidator(16)])
    expiration_date = models.DateField()
    cvv = models.CharField(max_length=3, validators=[MinLengthValidator(3), MaxLengthValidator(3)])

    def _str_(self):
        return f"Credit Card ending in {self.card_number[-4:]}"
    
class DoctorBooking(models.Model):
    PAYMENT_STATUS_PENDING = "P"
    PAYMENT_STATUS_COMPLETE = "C"
    PAYMENT_STATUS_FAILED = "F"

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, "Pending"),
        (PAYMENT_STATUS_COMPLETE, "Complete"),
        (PAYMENT_STATUS_FAILED, "Failed"),
    ]
    pending_status = models.CharField(
        max_length=50, choices=PAYMENT_STATUS_CHOICES, default="PAYMENT_STATUS_PENDING"
    )
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    booking_date = models.DateTimeField()
    is_cancelled = models.BooleanField(default=False)
    cancel_reason = models.CharField(max_length=200)
    payment_card = models.ForeignKey(CreditCard, on_delete=models.SET_NULL, blank=True,null=True)

    def __str__(self):
        return f"{self.patient.username}'s booking with Dr {self.doctor.username}"