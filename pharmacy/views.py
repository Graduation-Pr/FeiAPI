# rest imports
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import generics, status
# swagger imports
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# internal imports
from pharmacy.filters import PharmacyFilter, ProductFilter, DeviceFilter, MedicineFilter
from .models import Cart, CartItems, FavProduct, Pharmacy, Product, Device, Medicine
from .serializers import (
    SimpleMedicineListSerializer,
    SimpleDeviceListSerializer,
    UpdateCartItemSerializer,
    AddCartItemSerializer,
    FavProductSerializer,
    CartItemSerializer,
    MedicineSerializer,
    PharmacySerializer,
    ProductSerializer,
    DeviceSerializer,
    CartSerializer,
)


@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('pk', openapi.IN_PATH, description="Pharmacy ID", type=openapi.TYPE_INTEGER)
    ],
    responses={200: ProductSerializer(many=True)}
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_products(request, pk):
    """
    Retrieve all products for a given pharmacy.
    """
    try:
        pharmacy = Pharmacy.objects.get(id=pk)
    except Pharmacy.DoesNotExist:
        return Response(
            {"error": "Pharmacy with requested id not found"}, status=status.HTTP_404_NOT_FOUND
        )

    filterset = ProductFilter(
        request.GET, queryset=Product.objects.filter(pharmacy=pharmacy).order_by("id")
    )
    paginator = PageNumberPagination()
    paginator.page_size = 6
    queryset = paginator.paginate_queryset(filterset.qs, request)

    serializer = ProductSerializer(queryset, many=True)
    return paginator.get_paginated_response({"product": serializer.data})


@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('pk', openapi.IN_PATH, description="Pharmacy ID", type=openapi.TYPE_INTEGER)
    ],
    responses={200: SimpleDeviceListSerializer(many=True)}
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_devices(request, pk):
    """
    Retrieve all devices for a given pharmacy.
    """
    try:
        pharmacy = Pharmacy.objects.get(id=pk)
    except Pharmacy.DoesNotExist:
        return Response(
            {"error": "Pharmacy with requested id not found"}, status=status.HTTP_404_NOT_FOUND
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


@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('pk', openapi.IN_PATH, description="Pharmacy ID", type=openapi.TYPE_INTEGER)
    ],
    responses={200: SimpleMedicineListSerializer(many=True)}
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_medicines(request, pk):
    """
    Retrieve all medicines for a given pharmacy.
    """
    try:
        pharmacy = Pharmacy.objects.get(id=pk)
    except Pharmacy.DoesNotExist:
        return Response(
            {"error": "Pharmacy with requested id not found"}, status=status.HTTP_404_NOT_FOUND
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
    """
    Retrieve detailed information about a specific medicine.
    """
    permission_classes = (IsAuthenticated,)
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer


class DetailDevice(generics.RetrieveAPIView):
    """
    Retrieve detailed information about a specific device.
    """
    permission_classes = (IsAuthenticated,)
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


@swagger_auto_schema(
    method='get',
    responses={200: CartSerializer()}
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def cart_detail(request):
    """
    Retrieve the details of the current user's cart.
    """
    try:
        cart = Cart.objects.get(user=request.user)
        serializer = CartSerializer(cart, context={"request": request})
        return Response(serializer.data)
    except Cart.DoesNotExist:
        return Response({"message": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method='get',
    responses={200: CartItemSerializer()}
)
@swagger_auto_schema(
    method='patch',
    request_body=UpdateCartItemSerializer,
    responses={200: CartItemSerializer()}
)
@swagger_auto_schema(
    method='delete',
    responses={204: 'No Content'}
)
@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([IsAuthenticated])
def cart_item_detail(request, item_pk):
    """
    Retrieve, update, or delete a specific item in the current user's cart.
    """
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


@swagger_auto_schema(
    method='post',
    request_body=AddCartItemSerializer,
    responses={200: AddCartItemSerializer()}
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_cart_item(request):
    """
    Add an item to the current user's cart.
    """
    cart = Cart.objects.get(user=request.user)
    data = request.data
    serializer = AddCartItemSerializer(context={"cart_id": cart.id}, data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='get',
    responses={200: PharmacySerializer(many=True)}
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_pharmacies(request):
    """
    Retrieve a list of all pharmacies.
    """
    filterset = PharmacyFilter(
        request.GET, queryset=Pharmacy.objects.all().order_by("id")
    )
    paginator = PageNumberPagination()
    paginator.page_size = 6
    queryset = paginator.paginate_queryset(filterset.qs, request)

    serializer = PharmacySerializer(queryset, many=True, context={"request": request})
    return paginator.get_paginated_response({"pharmacy": serializer.data})


@swagger_auto_schema(
    method='post',
    manual_parameters=[
        openapi.Parameter('pk', openapi.IN_PATH, description="Product ID", type=openapi.TYPE_INTEGER)
    ],
    responses={200: FavProductSerializer()}
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_fav_product(request, pk):
    """
    Add a product to the current user's list of favorite products.
    """
    user = request.user
    try:
        product = Product.objects.get(id=pk)
        fav_product = FavProduct.objects.create(user=user, product=product)
        serializer = FavProductSerializer(fav_product, context={"request": request})
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    responses={200: FavProductSerializer(many=True)}
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_fav_produts(request):
    """
    Retrieve a list of the current user's favorite products.
    """
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
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return paginator.get_paginated_response(serializer.data)
