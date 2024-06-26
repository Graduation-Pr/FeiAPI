# internal imports
from pharmacy.serializers import SimpleProductSerializer
from .models import Order, OrderItem, CreditCard
from pharmacy.models import CartItems
from rest_framework import serializers
from django.db import transaction


class CreditCardSerializer(serializers.ModelSerializer):
    """
    Serializer for CreditCard model.
    """
    full_name = serializers.CharField(source="user.full_name", read_only=True)

    class Meta:
        model = CreditCard
        fields = ("id", "card_number", "full_name", "expiration_date", "card_type", "card_image", "cvv")

    def get_image_url(self, obj):
        """
        Method to get the absolute URL of the card image.
        """
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url"):
            return request.build_absolute_uri(obj.image.url)
        return None


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for OrderItem model.
    """
    product = SimpleProductSerializer()

    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity"]


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for Order model.
    """
    items = OrderItemSerializer(many=True, read_only=True)
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ["id", "placed_at", "owner", "items", "total_price", "pending_status"]

    def get_owner(self, obj):
        """
        Method to get the username of the order owner.
        """
        return obj.owner.username


class CreateOrderSerializer(serializers.Serializer):
    """
    Serializer for creating a new Order.
    """
    cart_id = serializers.UUIDField()

    def save(self, **kwargs):
        """
        Method to create an order from cart items.
        This method uses a database transaction to ensure atomicity.
        """
        with transaction.atomic():
            cart_id = self.validated_data["cart_id"]
            user_id = self.context["user_id"]
            order = Order.objects.create(owner_id=user_id)
            cart_items = CartItems.objects.filter(cart_id=cart_id)

            # Create order items from cart items
            order_items = [
                OrderItem(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                )
                for cart_item in cart_items
            ]
            OrderItem.objects.bulk_create(order_items)

            # Delete cart items after they are added to the order
            CartItems.objects.filter(cart_id=cart_id).delete()