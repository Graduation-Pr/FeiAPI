import uuid
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer, CreateOrderSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
import requests
from django.conf import settings
from rest_framework.response import Response

import json  # Add this import at the top of your file


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

    @action(detail=False, methods=["POST","GET"])
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
