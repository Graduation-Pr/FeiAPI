import uuid
from .models import Order, OrderItem, CreditCard
from .serializers import (
    CreditCardSerializer,
    OrderSerializer,
    OrderItemSerializer,
    CreateOrderSerializer,
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
import requests
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status


def initiate_payment(amount, email, order_id):
    url = "https://api.flutterwave.com/v3/payments"
    headers = {"Authorization": f"Bearer {settings.FLW_SEC_KEY}"}

    data = {
        "tx_ref": str(uuid.uuid4()),
        "amount": str(amount),
        "currency": "EGP",
        "redirect_url": "http://localhost:8000/orders/confirm_payment/?order_id="
        + str(order_id),
        "meta": {"consumer_id": 23, "consumer_mac": "92a3-912ba-1192a"},
        "customer": {
            "email": email,
            "phonenumber": "080****4528",
            "name": "Yemi Desola",
        },
        "customizations": {
            "title": "Pied Piper Payments",
            "logo": "http://www.piedpiper.com/app/themes/joystick-v27/images/logo.png",
        },
    }

    try:
        response = requests.post(url=url, headers=headers, json=data)
        response_data = response.json()
        return Response(response_data)

    except requests.exceptions.RequestException as err:
        print("Payment Went Wrong")
        return Response({"Error": str(err)}, status=500)


class OrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    @action(detail=True, methods=["POST"])
    def pay(self, request, pk):
        order = self.get_object()
        amount = order.total_price
        email = request.user.email
        order_id = order.id
        return initiate_payment(amount, email, order_id)

    @action(detail=False, methods=["POST", "GET"])
    def confirm_payment(self, request):
        order_id = request.GET.get("order_id")
        order = Order.objects.get(id=order_id)
        order.pending_status = "C"
        order.save()
        serializer = OrderSerializer(order)

        data = {"Message": "Payment Was Successeful", "data": serializer.data}
        return Response(data)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateOrderSerializer
        return OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(owner=user)

    def get_serializer_context(self):
        return {"user_id": self.request.user.id}


class OrderItemViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def list_credit_card(request):
    if request.method == "GET":
        user = request.user
        credit_cards = CreditCard.objects.filter(user=user)
        serializer = CreditCardSerializer(credit_cards, many=True)
        return Response(serializer.data)


@api_view(["GET", "DELETE"])
@permission_classes([IsAuthenticated])
def credit_card_detail(request, pk):
    user = request.user
    
    try:
        credit_card = CreditCard.objects.get(pk=pk)
    except CreditCard.DoesNotExist:
        return Response({"message":"card not found"},status=status.HTTP_404_NOT_FOUND)

    if credit_card.user == request.user:
        if request.method == "GET":
            serializer = CreditCardSerializer(credit_card)
            return Response(serializer.data)

        elif request.method == "DELETE":
            credit_card.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(
        {"errors": "this card isn't owned by this user"},
        status=status.HTTP_401_UNAUTHORIZED,
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def credit_card_create(request):
    user = request.user
    if request.method == "POST":
        serializer = CreditCardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors)
