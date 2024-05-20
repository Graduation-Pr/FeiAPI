from django.contrib import admin
from .models import PatientMedicine

@admin.register(PatientMedicine)
class PatientMedicineAdmin(admin.ModelAdmin):
    readonly_fields = ('end_date', 'start_date')