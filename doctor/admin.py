from django.contrib import admin
from .models import DoctorBooking, Service

admin.site.register(DoctorBooking)
admin.site.register(Service)
