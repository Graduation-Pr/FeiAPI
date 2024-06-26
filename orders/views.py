# internal imports
from .models import Order, OrderItem, CreditCard
from .serializers import (
    CreditCardSerializer,
    OrderSerializer,
    OrderItemSerializer,
    CreateOrderSerializer
)
# rest imports
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
# swagger imports
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



class OrderViewSet(ModelViewSet):
    """
    ViewSet for managing orders.
    """
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """
        Return different serializers based on the HTTP method.
        """
        if self.request.method == "POST":
            return CreateOrderSerializer
        return OrderSerializer

    def get_queryset(self):
        """
        Return different querysets based on the user role.
        """
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(owner=user)

    def get_serializer_context(self):
        """
        Provide additional context to the serializer.
        """
        return {"user_id": self.request.user.id}

    @swagger_auto_schema(
        method="post",
        operation_description="Make a payment for an order",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'payment_card': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the payment card')
            }
        ),
        responses={
            200: openapi.Response(description="Payment was successful", schema=OrderSerializer),
            400: openapi.Response(description="Bad Request"),
            404: openapi.Response(description="Payment card not found"),
        }
    )
    @action(detail=True, methods=["POST"])
    def pay(self, request, pk):
        """
        Custom action to handle payment for an order.
        """
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
        data = {"Message": "Payment Was Successful", "data": serializer.data}
        return Response(data)
class OrderItemViewSet(ModelViewSet):
    """
    ViewSet for managing order items.
    """
    permission_classes = [IsAuthenticated]
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


@swagger_auto_schema(
    method="get",
    operation_description="List all credit cards of the authenticated user",
    responses={200: CreditCardSerializer(many=True)},
)
@swagger_auto_schema(
    method="post",
    operation_description="Create a new credit card for the authenticated user",
    request_body=CreditCardSerializer,
    responses={201: CreditCardSerializer}
)
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def list_credit_card(request):
    """
    List or create credit cards for the authenticated user.
    """
    if request.method == "GET":
        user = request.user
        credit_cards = CreditCard.objects.filter(user=user)
        serializer = CreditCardSerializer(
            credit_cards, many=True, context={"request": request}
        )
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = CreditCardSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method="get",
    operation_description="Retrieve details of a specific credit card",
    responses={200: CreditCardSerializer}
)
@swagger_auto_schema(
    method="delete",
    operation_description="Delete a specific credit card",
    responses={204: "No Content"}
)
@api_view(["GET", "DELETE"])
@permission_classes([IsAuthenticated])
def credit_card_detail(request, pk):
    """
    Retrieve or delete a specific credit card.
    """
    user = request.user
    try:
        credit_card = CreditCard.objects.get(pk=pk)
    except CreditCard.DoesNotExist:
        return Response({"message": "Card not found"}, status=status.HTTP_404_NOT_FOUND)

    if credit_card.user == user:
        if request.method == "GET":
            serializer = CreditCardSerializer(credit_card)
            return Response(serializer.data)
        elif request.method == "DELETE":
            credit_card.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(
        {"errors": "This card isn't owned by this user"},
        status=status.HTTP_401_UNAUTHORIZED,
    )


@swagger_auto_schema(
    method="post",
    operation_description="Create a new credit card for the authenticated user",
    request_body=CreditCardSerializer,
    responses={201: CreditCardSerializer}
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def credit_card_create(request):
    """
    Create a new credit card.
    """
    if request.method == "POST":
        serializer = CreditCardSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)