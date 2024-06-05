from datetime import datetime
from django.db import models

# from accounts.models import User
from orders.models import CreditCard
from project import settings
from django.core.validators import MinValueValidator, MaxValueValidator


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


class DoctorComment(models.Model):
    text = models.CharField(max_length=200)
    booking = models.ForeignKey("DoctorBooking", on_delete=models.CASCADE, related_name="doctor_comment") 
    
    def __str__(self):
        return f"Dr {self.booking.doctor.username}'s comment for {self.booking.patient.username}"
    
    
class DoctorBooking(models.Model):
    STATUS_CHOICES = [
        ("upcoming", "Upcoming"),
        ("completed", "Completed"),
        ("canceled", "Canceled"),
    ]

    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="patient"
    )
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="doctor"
    )
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    booking_date = models.DateTimeField()
    payment_card = models.ForeignKey(
        CreditCard, on_delete=models.SET_NULL, blank=True, null=True
    )
    cancel_reason = models.CharField(max_length=200, null=True, blank=True)
    review = models.CharField(max_length=500, null=True, blank=True)
    rating = models.PositiveIntegerField(
        null=True, blank=True,default=0, validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="upcoming")

    def __str__(self):
        return f"{self.patient.username}'s booking with Dr {self.doctor.username}"


class PatientPlan(models.Model):
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="doctor_plan"
    )
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="patient_plan"
    )

    def __str__(self):
        return f"{self.patient.username}'s plan with Dr {self.doctor.username}"
