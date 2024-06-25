# django imports
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
# internal imports
from orders.models import CreditCard
from accounts.models import User


class Laboratory(models.Model):
    """
    Model representing a Laboratory with details such as name, image, location,
    rating, contact number, technology, and description.
    """
    # Choices for city field
    CITY_CHOICES = (
        ("MANS", "Mansoura"),
        ("NDAM", "New-Dammitta"),
        ("CAI", "Cairo"),
    )

    name = models.CharField(max_length=50, null=False, blank=False)  # Name of the laboratory
    image = models.ImageField(
        null=True, blank=True, upload_to="laboratory_pics", default="lab_icon.avif"
    )  # Image of the laboratory, defaulting to 'lab_icon.avif'
    city = models.CharField(
        max_length=100, choices=CITY_CHOICES, null=True, blank=True
    )  # City where the laboratory is located, with predefined choices
    rate = models.IntegerField(
        null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )  # Rating of the laboratory between 1 and 5
    phone_num = models.CharField(max_length=13)  # Contact phone number of the laboratory
    technology = models.CharField(max_length=50)  # Technology used by the laboratory
    about = models.TextField()  # Description about the laboratory

    def __str__(self):
        return self.name


# Choices for lab services
SERVICES = (
    ("D-Dimer", "D-Dimer"),
    ("CT. Scan", "CT. Scan"),
    ("Blood Test", "Blood Test"),
    ("Echo", "Echo"),
    ("X-ray", "X-ray"),
)


class LabService(models.Model):
    """
    Model representing a service offered by a laboratory, such as a blood test
    or an X-ray.
    """
    service = models.CharField(max_length=50, choices=SERVICES)  # Type of service provided
    price = models.PositiveBigIntegerField()  # Price of the service

    def __str__(self):
        return self.service


def lab_result_file_path(instance, filename):
    """
    Function to define the upload path for lab result files.
    Files will be uploaded to MEDIA_ROOT/lab_result/<patient_username>/<filename>
    """
    return f'lab_result/{instance.patient.username}/{filename}'


class LabBooking(models.Model):
    """
    Model representing a booking for a lab service, including details about
    the patient, lab, service, booking date, payment method, status, cancel reason,
    and lab result file.
    """
    # Choices for booking status
    STATUS_CHOICES = [
        ("upcoming", "Upcoming"),
        ("completed", "Completed"),
        ("canceled", "Canceled"),
    ]

    patient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="patient_lab"
    )  # Patient who booked the lab service
    lab = models.ForeignKey(
        Laboratory, on_delete=models.CASCADE, related_name="lab_booking"
    )  # Laboratory where the service is booked
    service = models.ForeignKey(LabService, on_delete=models.CASCADE)  # Service booked by the patient
    booking_date = models.DateTimeField()  # Date and time of the booking
    payment_card = models.ForeignKey(
        CreditCard, on_delete=models.SET_NULL, blank=True, null=True
    )  # Payment card used for the booking, can be null
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="upcoming"
    )  # Status of the booking, defaulting to 'upcoming'
    cancel_reason = models.CharField(max_length=200, null=True, blank=True)  # Reason for cancellation, if any
    lab_result = models.FileField(
        upload_to=lab_result_file_path, default='media/lab_result/lab_result1.pdf'
    )  # Lab result file, uploaded to a specific path

    def __str__(self):
        return f"{self.patient.username}'s booking with Lab {self.lab.name}"