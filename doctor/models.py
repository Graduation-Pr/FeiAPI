from datetime import datetime
from django.db import models
from accounts.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator
from orders.models import CreditCard


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


class DoctorBooking(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="patient")
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="doctor")
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    booking_date = models.DateTimeField()
    payment_card = models.ForeignKey(CreditCard, on_delete=models.SET_NULL, blank=True,null=True)
    is_cancelled = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    cancel_reason = models.CharField(max_length=200, null=True, blank=True)
    review = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"{self.patient.username}'s booking with Dr {self.doctor.username}"


class PatientPlan(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="doctor_plan")
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="patient_plan")
    
    
    def __str__(self):
        return f"{self.patient.username}'s plan with Dr {self.doctor.username}"
