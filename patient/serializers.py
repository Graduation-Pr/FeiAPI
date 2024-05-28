from rest_framework import serializers
from doctor.models import DoctorBooking
from laboratory.models import LabBooking
from orders.models import CreditCard


class DoctorBookingSerializer(serializers.ModelSerializer):
    doctor = serializers.CharField(read_only=True, source="doctor.full_name")
    patient = serializers.CharField(read_only=True, source="patient.full_name")
    payment_card = serializers.CharField(read_only=True)
    service_price = serializers.SerializerMethodField()

    class Meta:
        model = DoctorBooking
        fields = [
            "id",
            "doctor",
            "patient",
            "booking_date",
            "service",
            "payment_card",
            "status",
            "service_price",
            "rating",
        ]

    def get_service_price(self, obj):
        return obj.service.price

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


class LabBookingSerializer(serializers.ModelSerializer):
    lab = serializers.CharField(read_only=True)
    patient = serializers.CharField(read_only=True)
    payment_card = serializers.CharField(read_only=True)
    service_price = serializers.SerializerMethodField()

    class Meta:
        model = LabBooking
        fields = [
            "id",
            "lab",
            "patient",
            "booking_date",
            "service",
            "service_price",
            "payment_card",
        ]

    def create(self, validated_data):
        print("Context in Serializer:", self.context)
        patient_id = self.context["patient_id"]
        lab_id = self.context["lab_id"]
        payment_card_id = self.context["payment_card"]

        card = CreditCard.objects.get(id=payment_card_id)

        validated_data["lab_id"] = lab_id
        validated_data["patient_id"] = patient_id
        validated_data["payment_card"] = card
        return super().create(validated_data)

    def get_service_price(self, obj):
        return obj.service.price
