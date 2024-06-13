from django.contrib import admin
from .models import PatientMedicine, Test, Question

admin.site.register(Question)


@admin.register(PatientMedicine)
class PatientMedicineAdmin(admin.ModelAdmin):
    readonly_fields = ('end_date', 'start_date', "quantity")
    
@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    readonly_fields = ("date",)