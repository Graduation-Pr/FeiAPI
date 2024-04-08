from rest_framework import serializers
from doctor.models import DoctorBooking
from doctor.models import CreditCard


class CreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCard
        fields = ('id', 'card_number', 'expiration_date','cvv')


class DoctorWriteBookingSerializer(serializers.ModelSerializer):
    doctor = serializers.CharField(read_only=True)
    id = serializers.CharField(read_only=True)
    patient = serializers.CharField(read_only=True)
    
    class Meta:
        model = DoctorBooking
        fields = (
            "id",
            "doctor",
            "patient",
            "service",
            "booking_date",
        )

    def create(self, validated_data):
        user_id = self.context["user_id"]
        doctor_id = self.context["doctor_id"]
        validated_data["doctor_id"] = doctor_id
        validated_data["patient_id"] = user_id
        return super().create(validated_data)



class BookingOrderSerializer(serializers.ModelSerializer):
    doctor = serializers.CharField(read_only=True)
    patient = serializers.CharField(read_only=True)
    service = serializers.CharField(read_only=True)
    payment_card = CreditCardSerializer(required=False)
    
    class Meta:
        model = DoctorBooking
        fields = ["id", "pending_status", "doctor", "patient","service","booking_date", "payment_card"]


    
# class CreateOrderSerializer(serializers.Serializer):
#     cart_id = serializers.UUIDField()

#     def save(self, **kwargs):
#         with transaction.atomic():
#             order = Order.objects.create(owner_id=user_id)

            # order_items = [
            #     OrderItem(
            #         order=order,
            #         product=cart_item.product,
            #         quantity=cart_item.quantity,
            #     )
            #     for cart_item in cart_items
            # ]
            # OrderItem.objects.bulk_create(order_items)

            # [
            #     CartItems.objects.filter(cart_id=cart_id).delete()
            #     for cart_item in cart_items
            # ]
