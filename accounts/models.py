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
    reset_password_token = models.CharField(max_length=50, default="", blank=True)
    reset_password_expire = models.DateTimeField(null =True, blank=True)
    def __str__(self):
        return self.username


class PatientProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="patient_profile"
    )

    def __str__(self):
        return f"{self.user.username}'s Patient Profile"


class DoctorProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="doctor_profile"
    )

    def __str__(self):
        return f"{self.user.username}'s Doctor Profile"


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == User.Role.PATIENT:
            PatientProfile.objects.create(user=instance)
        elif instance.role == User.Role.DOCTOR:
            DoctorProfile.objects.create(user=instance)
