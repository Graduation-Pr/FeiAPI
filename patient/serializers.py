from rest_framework import serializers
from doctor.models import DoctorBooking
from orders.serializers import CreditCardSerializer
from orders.models import CreditCard

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
    payment_card = CreditCardSerializer(read_only=True)
    # payment_card = serializers.SerializerMethodField()
    # card_id = serializers.CharField()

    class Meta:
        model = DoctorBooking
        fields = [
            "id",
            "doctor",
            "patient",
            "service",
            "booking_date",
            "payment_card",
            # "card_id",
        ]
        
    # def get_payment_card(self, card_id):
    #     card = CreditCard.objects.get(id=card_id)
    #     self.validated_data["payment_card"] = card


