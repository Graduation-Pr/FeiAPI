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


class OrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    @action(detail=True, methods=["POST"])
    def pay(self, request, pk):
        order = self.get_object()
        data = request.data
        user = request.user
        try:
            payment_card = data["payment_card"]
            card = CreditCard.objects.get(id=payment_card)
            if card.user != user:
                return Response(
                    {"errors": "You are not the owner of this card"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except KeyError:
            return Response(
                {"errors": "Payment card ID is missing"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except CreditCard.DoesNotExist:
            return Response(
                {"errors": "Payment card not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )
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
        serializer = CreditCardSerializer(
            credit_cards, many=True, context={"request": request}
        )
        return Response(serializer.data)


@api_view(["GET", "DELETE"])
@permission_classes([IsAuthenticated])
def credit_card_detail(request, pk):
    user = request.user

    try:
        credit_card = CreditCard.objects.get(pk=pk)
    except CreditCard.DoesNotExist:
        return Response({"message": "card not found"}, status=status.HTTP_404_NOT_FOUND)

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
        serializer = CreditCardSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save(user=user)
            return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors)
