from rest_framework import serializers
from .models import FavProduct, Pharmacy, Product, Cart, CartItems, Medicine, Device


class ProductSerializer(serializers.ModelSerializer):
    pharmacy = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ("id", "name", "price", "pharmacy", "description")

    def get_pharmacy(self, obj):
        return obj.pharmacy.name


class SimpleMedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = ("name", "pill_dosage")


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
            "is_fav",
            "pill_dosage",
            "category",
            "subcategory",
        )


class SimpleMedicineListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = (
            "id",
            "name",
            "price",
            "image",
            "is_fav",
        )

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url"):
            return request.build_absolute_uri(obj.image.url)
        return None


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
            "is_fav",
            "category",
            "subcategory",
        )


class SimpleDeviceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = (
            "id",
            "name",
            "price",
            "image",
            "is_fav",
        )

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url"):
            return request.build_absolute_uri(obj.image.url)
        return None


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "image",
            "price",
        ]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url"):
            return request.build_absolute_uri(obj.image.url)
        return None


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    sub_total = serializers.SerializerMethodField(method_name="total")

    class Meta:
        model = CartItems
        fields = ["id", "product", "quantity", "sub_total"]

    def total(self, cart_item: CartItems):
        return cart_item.quantity * cart_item.product.price


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    grand_total = serializers.SerializerMethodField(method_name="main_total")

    class Meta:
        model = Cart
        fields = ["id", "items", "grand_total"]

    def main_total(self, cart: Cart):
        items = cart.items.all()
        total = sum([item.quantity * item.product.price for item in items])
        return total


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError(
                "There is no product associated with the given ID"
            )

        return value

    def save(self, **kwargs):
        cart_id = self.context["cart_id"]
        product_id = self.validated_data["product_id"]
        quantity = self.validated_data["quantity"]

        try:
            cartitem = CartItems.objects.get(product_id=product_id, cart_id=cart_id)
            cartitem.quantity += quantity
            cartitem.save()

            self.instance = cartitem

        except:
            self.instance = CartItems.objects.create(
                cart_id=cart_id, **self.validated_data
            )

        return self.instance

    class Meta:
        model = CartItems
        fields = ["id", "product_id", "quantity"]


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItems
        fields = ["quantity"]


class PharmacySerializer(serializers.ModelSerializer):

    class Meta:
        model = Pharmacy
        fields = "__all__"

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url"):
            return request.build_absolute_uri(obj.image.url)
        return None


class FavProductSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    class Meta:
        model = FavProduct
        fields = ("id", "user", "product")

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url"):
            return request.build_absolute_uri(obj.image.url)
        return None
