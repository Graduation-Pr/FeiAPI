from datetime import timedelta
from django.db import models
from pharmacy.models import Medicine
from doctor.models import PatientPlan
from django.core.exceptions import ValidationError

class PatientMedicine(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name="patient_medicine")
    dose = models.PositiveIntegerField()
    program = models.PositiveIntegerField()  # duration in weeks
    plan = models.ForeignKey(PatientPlan, on_delete=models.CASCADE, related_name="medicine_plan")
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(blank=True, null=True)

    def clean(self):
        if not self.program:
            raise ValidationError('Program duration is required')

    def save(self, *args, **kwargs):
        # Validate before saving
        self.clean()
        
        # Save the object first to ensure start_date is set
        super().save(*args, **kwargs)

        # Now calculate end_date based on start_date and program
        if self.start_date and self.program:
            self.end_date = self.start_date + timedelta(weeks=self.program)
            # Save the object again to store the calculated end_date
            super().save(update_fields=['end_date'])
            
            
    def __str__(self):
        return f"{self.medicine.name} for {self.dose} times a day"
