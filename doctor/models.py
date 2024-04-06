from datetime import datetime
from django.db import models
from accounts.models import User


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
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    booking_date = models.DateTimeField()
    

    def __str__(self):
        return f"{self.patient.username}'s booking with Dr {self.doctor.username}"

