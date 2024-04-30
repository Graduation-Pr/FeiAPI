from rest_framework import serializers
from doctor.models import DoctorBooking
from orders.models import CreditCard


class DoctorBookingSerializer(serializers.ModelSerializer):
    doctor = serializers.CharField(read_only=True)
    patient = serializers.CharField(read_only=True)
    payment_card = serializers.CharField(read_only=True)


    class Meta:
        model = DoctorBooking
        fields = ["id", "doctor", "patient", "booking_date", "service", "payment_card"]


    def create(self, validated_data):
        print("Context in Serializer:", self.context)
        patient_id = self.context["patient_id"]
        doctor_id = self.context["doctor_id"]
        payment_card_id = self.context["payment_card"]

        card = CreditCard.objects.get(id=payment_card_id)

        validated_data["doctor_id"] = doctor_id
        validated_data["patient_id"] = patient_id
        validated_data["payment_card"] = card
        return super().create(validated_data)


