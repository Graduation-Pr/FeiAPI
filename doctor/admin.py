from django.contrib import admin
from .models import DoctorBooking, Service, PatientPlan, DoctorComment

admin.site.register(DoctorBooking)
admin.site.register(Service)
admin.site.register(PatientPlan) 
admin.site.register(DoctorComment) 

