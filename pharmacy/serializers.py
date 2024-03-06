from rest_framework import serializers
from .models import Category, Product
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
        
        
class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = '__all__'
