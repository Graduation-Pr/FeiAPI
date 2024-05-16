from django.shortcuts import render
from rest_framework import generics
from pharmacy.filters import ProductFilter, DeviceFilter, MedicineFilter
from .models import Cart, CartItems, Product, Device, Medicine
from .serializers import (
    AddCartItemSerializer,
    CartItemSerializer,
    CartSerializer,
    ProductSerializer,
    UpdateCartItemSerializer,
    MedicineSerializer,
    DeviceSerializer,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_products(request):
    filterset = ProductFilter(
        request.GET, queryset=Product.objects.all().order_by("id")
    )
    paginator = PageNumberPagination()
    paginator.page_size = 6
    queryset = paginator.paginate_queryset(filterset.qs, request)

    serializer = ProductSerializer(queryset, many=True)
    return paginator.get_paginated_response({"product": serializer.data})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_devices(request):
    filterset = DeviceFilter(request.GET, queryset=Device.objects.all().order_by("id"))
    paginator = PageNumberPagination()
    paginator.page_size = 6
    queryset = paginator.paginate_queryset(filterset.qs, request)

    serializer = DeviceSerializer(queryset, many=True)
    return paginator.get_paginated_response({"devices": serializer.data})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_medicines(request):
    filterset = MedicineFilter(
        request.GET, queryset=Medicine.objects.all().order_by("id")
    )
    paginator = PageNumberPagination()
    paginator.page_size = 6
    queryset = paginator.paginate_queryset(filterset.qs, request)

    serializer = MedicineSerializer(queryset, many=True)
    return paginator.get_paginated_response({"medicines": serializer.data})


class DetailMedicine(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer


class DetailDevice(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


# class CartViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
#     permission_classes = (permissions.IsAuthenticated,)
#     # queryset = Cart.objects.all()
#     serializer_class = CartSerializer

#     def get_queryset(self):
#         # Retrieve the cart associated with the authenticated user
#         user = self.request.user
#         return Cart.objects.filter(user=user)


# class CartItemsViewSet(ModelViewSet):
#     http_method_names = ["get", "post", "patch", "delete"]

#     permission_classes = (permissions.IsAuthenticated,)

#     def get_queryset(self):
#         return CartItems.objects.filter(cart_id=self.kwargs["cart_pk"])

#     def get_serializer_class(self):
#         if self.request.method == "POST":
#             return AddCartItemSerializer
#         elif self.request.method == "PATCH":
#             return UpdateCartItemSerializer
#         return CartItemSerializer

#     def get_serializer_context(self):
#         return {"cart_id": self.kwargs["cart_pk"]}

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItems
from .serializers import CartSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer
from rest_framework.permissions import IsAuthenticated

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def cart_detail(request):
        try:
            cart = Cart.objects.get(user=request.user)
            serializer = CartSerializer(cart)
            return Response(serializer.data)
        except Cart.DoesNotExist:
            return Response({"message": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def cart_item_detail(request, item_pk):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        return Response({"message": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
    try:
        cart_item = CartItems.objects.get(pk=item_pk, cart_id=cart.id)
    except CartItems.DoesNotExist:
        return Response({"message": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)
    
    elif request.method == "PATCH":
        serializer = UpdateCartItemSerializer(cart_item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_cart_item(request):
    cart = Cart.objects.get(user=request.user)
    data = request.data
    serializer = AddCartItemSerializer(context={"cart_id":cart.id}, data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors)
    