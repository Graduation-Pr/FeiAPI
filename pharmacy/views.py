from django.shortcuts import render
from rest_framework import generics
#from django.contrib.auth.models import User
from .models import Category, Product
from .serializers import ProductSerializer, CategorySerializer
from rest_framework import permissions
from rest_framework.response import Response



class ListProduct(generics.ListCreateAPIView):    
    #permission_classes = (permissions.IsAuthenticated,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class DetailProduct(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = (permissions.IsAuthenticated,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    
    
class ListCategory(generics.ListCreateAPIView):
    #permission_classes = (permissions.IsAuthenticated,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class DetailCategory(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = (permissions.IsAuthenticated,)
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    
