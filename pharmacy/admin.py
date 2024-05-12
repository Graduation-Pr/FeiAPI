from django.contrib import admin
from .models import Pharmacy, Device, Cart, Medicine

# Register your models here.
admin.site.register(Device)
admin.site.register(Pharmacy)
admin.site.register(Cart)
admin.site.register(Medicine)
