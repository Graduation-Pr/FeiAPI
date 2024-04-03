from datetime import datetime
from django.db import models
from accounts.models import PatientProfile, DoctorProfile


PACKAGES = (
    ("Messaging", "Messaging"),
    ("Voice call", "Voice call"),
    ("In person", "In person"),
)


class DoctorBooking(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    service = models.CharField(max_length=50, choices=PACKAGES)
    booking_day = models.DateField()
    booking_hour = models.DateTimeField()
    time_ordered = models.DateTimeField(default=datetime.now)
    duration = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.patient}'s booking with Dr {self.doctor}"
