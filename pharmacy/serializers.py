from .models import FavProduct, Pharmacy, Product, Cart, CartItems, Medicine, Device
from rest_framework import serializers


# Serializer for the Product model
class ProductSerializer(serializers.ModelSerializer):
    # Custom field to get the pharmacy name
    pharmacy = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ("id", "name", "price", "pharmacy", "description")

    # Method to get the pharmacy name
    def get_pharmacy(self, obj):
        return obj.pharmacy.name

# Simple serializer for the Medicine model
class SimpleMedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ("name", "pill_dosage")

# Detailed serializer for the Medicine model
class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = (
            "id",
            "name",
            "description",
            "price",
            "stock",
            "image",
            "pill_dosage",
            "category",
            "subcategory",
        )

# Simple list serializer for the Medicine model
class SimpleMedicineListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = (
            "id",
            "name",
            "price",
            "image",
        )

    # Method to get the full image URL
    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url"):
            return request.build_absolute_uri(obj.image.url)
        return None

# Detailed serializer for the Device model
class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = (
            "id",
            "name",
            "description",
            "price",
            "stock",
            "image",
            "category",
            "subcategory",
        )

# Simple list serializer for the Device model
class SimpleDeviceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = (
            "id",
            "name",
            "price",
            "image",
        )

    # Method to get the full image URL
    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url"):
            return request.build_absolute_uri(obj.image.url)
        return None

# Simple serializer for the Product model
class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "image",
            "price",
        ]

    # Method to get the full image URL
    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url"):
            return request.build_absolute_uri(obj.image.url)
        return None

# Serializer for the CartItems model
class CartItemSerializer(serializers.ModelSerializer):
    # Nested serializer for the product
    product = SimpleProductSerializer()
    # Custom field to calculate the subtotal
    sub_total = serializers.SerializerMethodField(method_name="total")

    class Meta:
        model = CartItems
        fields = ["id", "product", "quantity", "sub_total"]

    # Method to calculate the subtotal
    def total(self, cart_item: CartItems):
        return cart_item.quantity * cart_item.product.price

# Serializer for the Cart model
class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    # Nested serializer for cart items
    items = CartItemSerializer(many=True, read_only=True)
    # Custom field to calculate the grand total
    grand_total = serializers.SerializerMethodField(method_name="main_total")

    class Meta:
        model = Cart
        fields = ["id", "items", "grand_total"]

    # Method to calculate the grand total
    def main_total(self, cart: Cart):
        items = cart.items.all()
        total = sum([item.quantity * item.product.price for item in items])
        return total

# Serializer for adding items to the cart
class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    # Validation method for product ID
    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError(
                "There is no product associated with the given ID"
            )
        return value

    # Method to save the cart item
    def save(self, **kwargs):
        cart_id = self.context["cart_id"]
        product_id = self.validated_data["product_id"]
        quantity = self.validated_data["quantity"]

        try:
            cartitem = CartItems.objects.get(product_id=product_id, cart_id=cart_id)
            cartitem.quantity += quantity
            cartitem.save()
            self.instance = cartitem
        except CartItems.DoesNotExist:
            self.instance = CartItems.objects.create(
                cart_id=cart_id, **self.validated_data
            )

        return self.instance

    class Meta:
        model = CartItems
        fields = ["id", "product_id", "quantity"]

# Serializer for updating items in the cart
class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItems
        fields = ["quantity"]

# Serializer for the Pharmacy model
class PharmacySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacy
        fields = "__all__"

    # Method to get the full image URL
    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url"):
            return request.build_absolute_uri(obj.image.url)
        return None

# Serializer for the FavProduct model
class FavProductSerializer(serializers.ModelSerializer):
    # Nested serializer for the product
    product = SimpleProductSerializer()

    class Meta:
        model = FavProduct
        fields = ("id", "user", "product")

    # Method to get the full image URL
    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url"):
            return request.build_absolute_uri(obj.image.url)
        return None