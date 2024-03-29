from rest_framework import serializers
from .models import Order, OrderItem
from pharmacy.serializers import SimpleProductSerializer
from pharmacy.models import CartItems, Cart
from django.db import transaction


class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "placed_at", "pending_status", "owner", "items"]


class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data["cart_id"]
            user_id = self.context["user_id"]
            order = Order.objects.create(owner_id=user_id)
            cart_items = CartItems.objects.filter(cart_id=cart_id)
            order_items = [
                OrderItem(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                )
                for cart_item in cart_items
            ]
            OrderItem.objects.bulk_create(order_items)

            [
                CartItems.objects.filter(cart_id=cart_id).delete()
                for cart_item in cart_items
            ]
