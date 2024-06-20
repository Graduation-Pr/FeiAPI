from django.contrib import admin
from .models import DoctorBooking, Service, PatientPlan, DoctorComment, Prescription

admin.site.register(DoctorBooking)
admin.site.register(Service)
admin.site.register(PatientPlan) 
admin.site.register(DoctorComment) 
admin.site.register(Prescription) 

