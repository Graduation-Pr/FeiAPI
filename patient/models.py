# internal imports
from doctor.models import DoctorBooking, PatientPlan
from pharmacy.models import Medicine
# django imports
from django.core.exceptions import ValidationError
from django.db import models
# python import
from datetime import timedelta


class PatientMedicine(models.Model):
    """
    Model to store patient's prescribed medicines with dosage and program duration.
    """
    medicine = models.ForeignKey(
        Medicine, on_delete=models.CASCADE, related_name="patient_medicine"
    )
    dose = models.PositiveIntegerField()
    program = models.PositiveIntegerField()  # duration in weeks
    plan = models.ForeignKey(
        PatientPlan, on_delete=models.CASCADE, related_name="medicine_plan"
    )
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(blank=True, null=True)
    quantity = models.PositiveIntegerField(blank=True, null=True)
    left = models.PositiveIntegerField(blank=True, null=True)

    def clean(self):
        """
        Ensure program duration is provided.
        """
        if not self.program:
            raise ValidationError("Program duration is required")

    def save(self, *args, **kwargs):
        """
        Custom save method to calculate and set the quantity, left, and end_date fields.
        """
        # Check if the object is being created (self.pk is None if it is a new object)
        is_new = self.pk is None

        # Validate before saving
        self.clean()

        # Save the object first to ensure start_date is set
        super().save(*args, **kwargs)

        if is_new and self.start_date and self.program:
            # Calculate quantity and left based on dose and program
            total_doses = self.dose * self.program * 7  # assuming dose is per day and program is in weeks
            self.quantity = total_doses
            self.left = total_doses  # Set left to the total doses initially
            self.end_date = self.start_date + timedelta(weeks=self.program)

            # Save the object again to store the calculated fields
            super().save(update_fields=["end_date", "quantity", "left"])

    def __str__(self):
        return f"{self.medicine.name} for {self.dose} times a day"

class Test(models.Model):
    """
    Model to store medical tests related to a doctor's booking.
    """
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    booking = models.ForeignKey(DoctorBooking, related_name="test_booking", on_delete=models.CASCADE)

    def __str__(self):
        return f"Dr {self.booking.doctor.username}'s test for {self.booking.patient.username} at {self.date}"

class Question(models.Model):
    """
    Model to store questions related to a medical test.
    """
    text = models.CharField(max_length=200)
    answer = models.BooleanField(null=True, blank=True)
    test = models.ForeignKey(Test, related_name='questions', on_delete=models.CASCADE)

    def __str__(self):
        return self.text