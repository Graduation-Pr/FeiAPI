from django.contrib import admin
from .models import Laboratory, LabService, LabBooking

admin.site.register(Laboratory)
admin.site.register(LabBooking)
admin.site.register(LabService)
