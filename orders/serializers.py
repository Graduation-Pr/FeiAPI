from rest_framework import serializers
from .models import Order, OrderItem, CreditCard
from pharmacy.serializers import SimpleProductSerializer
from pharmacy.models import CartItems
from django.db import transaction
from accounts.models import User


class CreditCardSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="user.full_name", read_only=True)

    class Meta:
        model = CreditCard
        fields = ("id", "card_number", "full_name", "expiration_date", "card_type", "card_image", "cvv")

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url"):
            return request.build_absolute_uri(obj.image.url)
        return None
    


    


class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ["id", "placed_at", "owner", "items", "total_price", "pending_status"]

    def get_owner(self, obj):
        return obj.owner.username


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
