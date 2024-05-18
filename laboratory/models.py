from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from accounts.models import User
from orders.models import CreditCard


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
    # patient = models.PositiveIntegerField()
    
    def __str__(self):
        return self.name
    
    
SERVICES = (
    ("D-Dimer", "D-Dimer"),
    ("CT. Scan", "CT. Scan"),
    ("Blood Test", "Blood Test"),
    ("Echo", "Echo"),
    ("X-ray", "X-ray"),
)


class LabService(models.Model):
    service = models.CharField(max_length=50, choices=SERVICES)
    price = models.PositiveBigIntegerField()

    def __str__(self):
        return f"{self.service}"


class LabBooking(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="patient_lab")
    lab = models.ForeignKey(Laboratory, on_delete=models.CASCADE, related_name="lab_booking")
    service = models.ForeignKey(LabService, on_delete=models.CASCADE)
    booking_date = models.DateTimeField()
    payment_card = models.ForeignKey(CreditCard, on_delete=models.SET_NULL, blank=True,null=True)
    is_cancelled = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    cancel_reason = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.patient.username}'s booking with Lab {self.lab.name}"

