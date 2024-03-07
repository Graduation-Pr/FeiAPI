from django.shortcuts import render
from rest_framework import generics
#from django.contrib.auth.models import User
from .models import Product
from .serializers import ProductSerializer
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
    
    
    
