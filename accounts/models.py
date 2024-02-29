from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        PATIENT = "PATIENT", "Patient"
        DOCTOR = "DOCTOR", "Doctor"

    role = models.CharField(choices=Role.choices, max_length=10, default=Role.PATIENT)

    def __str__(self):
        return self.username


class PatientProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="patient_profile"
    )
    # Add relevant patient-specific fields here
    # For example:
    # date_of_birth = models.DateField(blank=True, null=True)
    # phone_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Patient Profile"


class DoctorProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="doctor_profile"
    )
    # Add relevant doctor-specific fields here
    # For example:
    # specialty = models.CharField(max_length=50, blank=True)
    # hospital = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Doctor Profile"


# Signals to create profiles automatically upon user creation


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == User.Role.PATIENT:
            PatientProfile.objects.create(user=instance)
        elif instance.role == User.Role.DOCTOR:
            DoctorProfile.objects.create(user=instance)
