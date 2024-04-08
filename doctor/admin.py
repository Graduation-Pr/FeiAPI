from django.contrib import admin
from .models import DoctorBooking, Service, CreditCard

admin.site.register(DoctorBooking)
admin.site.register(Service)
admin.site.register(CreditCard)
