from django.contrib import admin
from .models import Pharmacy, Product, Cart

# Register your models here.
admin.site.register(Product)
admin.site.register(Pharmacy)
admin.site.register(Cart)
