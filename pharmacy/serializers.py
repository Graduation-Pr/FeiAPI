from rest_framework import serializers
from .models import Product
from accounts.models import User


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'name',
            'description',
            'category',
            'price',
            'stock',
            'image',
        )
        
