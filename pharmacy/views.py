from rest_framework import generics
from pharmacy.filters import PharmacyFilter, ProductFilter, DeviceFilter, MedicineFilter
from .models import Cart, CartItems, FavProduct, Pharmacy, Product, Device, Medicine
from .serializers import (
    AddCartItemSerializer,
    CartItemSerializer,
    CartSerializer,
    FavProductSerializer,
    PharmacySerializer,
    ProductSerializer,
    SimpleDeviceListSerializer,
    SimpleMedicineListSerializer,
    UpdateCartItemSerializer,
    MedicineSerializer,
    DeviceSerializer,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItems
from .serializers import (
    CartSerializer,
    CartItemSerializer,
    AddCartItemSerializer,
    UpdateCartItemSerializer,
)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_products(request, pk):
    try:
        pharmacy = Pharmacy.objects.get(id=pk)
    except Pharmacy.DoesNotExist:
        return Response(
            "pharmacy with requested id not found", status=status.HTTP_404_NOT_FOUND
        )
    filterset = ProductFilter(
        request.GET, queryset=Product.objects.filter(pharmacy=pharmacy).order_by("id")
    )
    paginator = PageNumberPagination()
    paginator.page_size = 6
    queryset = paginator.paginate_queryset(filterset.qs, request)

    serializer = ProductSerializer(queryset, many=True)
    return paginator.get_paginated_response({"product": serializer.data})



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_devices(request, pk):
    try:
        pharmacy = Pharmacy.objects.get(id=pk)
    except Pharmacy.DoesNotExist:
        return Response(
            "pharmacy with requested id not found", status=status.HTTP_404_NOT_FOUND
        )
    filterset = DeviceFilter(
        request.GET, queryset=Device.objects.filter(pharmacy=pharmacy).order_by("id")
    )
    paginator = PageNumberPagination()
    paginator.page_size = 6
    queryset = paginator.paginate_queryset(filterset.qs, request)

    serializer = SimpleDeviceListSerializer(
        queryset, many=True, context={"request": request}
    )
    return paginator.get_paginated_response({"devices": serializer.data})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_medicines(request, pk):
    try:
        pharmacy = Pharmacy.objects.get(id=pk)
    except Pharmacy.DoesNotExist:
        return Response(
            "pharmacy with requested id not found", status=status.HTTP_404_NOT_FOUND
        )
    filterset = MedicineFilter(
        request.GET, queryset=Medicine.objects.filter(pharmacy=pharmacy).order_by("id")
    )
    paginator = PageNumberPagination()
    paginator.page_size = 6
    queryset = paginator.paginate_queryset(filterset.qs, request)

    serializer = SimpleMedicineListSerializer(
        queryset, many=True, context={"request": request}
    )
    return paginator.get_paginated_response({"medicines": serializer.data})


class DetailMedicine(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer


class DetailDevice(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def cart_detail(request):
    try:
        cart = Cart.objects.get(user=request.user)
        serializer = CartSerializer(cart, context={"request": request})
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
        return Response(
            {"message": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "GET":
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)

    elif request.method == "PATCH":
        serializer = UpdateCartItemSerializer(
            cart_item, data=request.data, partial=True
        )
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
    serializer = AddCartItemSerializer(context={"cart_id": cart.id}, data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_pharmacies(request):
    filterset = PharmacyFilter(
        request.GET, queryset=Pharmacy.objects.all().order_by("id")
    )
    paginator = PageNumberPagination()
    paginator.page_size = 6
    queryset = paginator.paginate_queryset(filterset.qs, request)

    serializer = PharmacySerializer(queryset, many=True, context={"request": request})
    return paginator.get_paginated_response({"pharmacy": serializer.data})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_fav_product(request, pk):
    user = request.user
    try:
        product = Product.objects.get(id=pk)
        fav_product = FavProduct.objects.create(user=user, product=product)
        serializer = FavProductSerializer(fav_product, context={"request": request})
    except Exception as e:
        return Response({"errros": e})
    return Response(serializer.data, status=200)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_fav_produts(request):
    user = request.user
    try:
        fav_products = FavProduct.objects.filter(user=user)
        paginator = PageNumberPagination()
        paginator.page_size = 5
        query_set = paginator.paginate_queryset(list(fav_products), request)
        serializer = FavProductSerializer(
            query_set, many=True, context={"request": request}
        )
    except Exception as e:
        return Response({"errros": e})

    return paginator.get_paginated_response(serializer.data)
