from django.contrib import admin
from .models import Order, CreditCard


admin.site.register(Order)
admin.site.register(CreditCard)
# admin.site.register(OrderItem)
