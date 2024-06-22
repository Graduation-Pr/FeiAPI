# django imports
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
# internal imports
from orders.models import CreditCard
from project import settings


# Choices for different types of services
SERVICES = (
    ("Standard Appointment", "Standard Appointment"),
    ("Specialist Consultations", "Specialist Consultations"),
    ("Follow-up Appointment", "Follow-up Appointment"),
)

# Model representing a service offered by a doctor
class Service(models.Model):
    service = models.CharField(max_length=50, choices=SERVICES)
    price = models.PositiveBigIntegerField()

    def __str__(self):
        return self.service

# Model representing a comment by a doctor about a specific booking
class DoctorComment(models.Model):
    text = models.CharField(max_length=200)
    booking = models.ForeignKey(
        "DoctorBooking", on_delete=models.CASCADE, related_name="doctor_comment"
    )

    def __str__(self):
        return f"Dr {self.booking.doctor.username}'s comment for {self.booking.patient.username}"

# Model representing a booking between a patient and a doctor
class DoctorBooking(models.Model):
    STATUS_CHOICES = [
        ("upcoming", "Upcoming"),
        ("completed", "Completed"),
        ("canceled", "Canceled"),
    ]

    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="patient_bookings"
    )
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="doctor_bookings"
    )
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    booking_date = models.DateTimeField()
    payment_card = models.ForeignKey(
        CreditCard, on_delete=models.SET_NULL, blank=True, null=True
    )
    cancel_reason = models.CharField(max_length=200, null=True, blank=True)
    review = models.CharField(max_length=500, null=True, blank=True)
    rating = models.PositiveIntegerField(
        null=True, blank=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="upcoming")

    def __str__(self):
        return f"{self.patient.username}'s booking with Dr {self.doctor.username}"

# Model representing a care plan assigned by a doctor to a patient
class PatientPlan(models.Model):
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="doctor_plans"
    )
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="patient_plans"
    )

    def __str__(self):
        return f"{self.patient.username}'s plan with Dr {self.doctor.username}"

# Model representing a prescription related to a patient's care plan
class Prescription(models.Model):
    patient_plan = models.ForeignKey(
        PatientPlan, on_delete=models.CASCADE, related_name="prescriptions"
    )
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient_plan.patient.username}'s prescription with Dr {self.patient_plan.doctor.username}"