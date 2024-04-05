from datetime import datetime
from django.db import models
from accounts.models import PatientProfile, DoctorProfile


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
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    booking_day = models.DateField()
    booking_hour = models.DateTimeField()
    

    def __str__(self):
        return f"{self.patient.user.username}'s booking with Dr {self.doctor.user.username}"

