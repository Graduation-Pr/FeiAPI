from rest_framework import serializers
from doctor.models import DoctorBooking
from accounts.models import User

class DoctorBookingNameSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    class Meta:
        model = User
        fields = ("first_name", "last_name")

class DoctorWriteBookingChatAndVoiceSerializer(serializers.ModelSerializer):
    doctor = DoctorBookingNameSerializer(read_only=True)
    id = serializers.CharField(read_only=True)


    class Meta:
        model = DoctorBooking
        fields = (
            "id",
            "service",
            "booking_day",
            "booking_hour",
            "time_ordered",
            "duration",
            "doctor"
        )

    def create(self, validated_data):
        user_id = self.context["user_id"]
        doctor_id = self.context["doctor_id"]
        validated_data["doctor_id"] = doctor_id
        validated_data["patient_id"] = user_id
        return super().create(validated_data)


class DoctorWriteBookingInPersonSerializer(serializers.ModelSerializer):
    doctor = serializers.CharField(read_only=True)
    id = serializers.CharField(read_only=True)
    duration = serializers.CharField(read_only=True)

    class Meta:
        model = DoctorBooking
        fields = (
            "id",
            "service",
            "booking_day",
            "booking_hour",
            "time_ordered",
            "duration",
            "doctor",
        )

    def create(self, validated_data):
        user_id = self.context["user_id"]
        doctor_id = self.context["doctor_id"]
        validated_data["doctor_id"] = doctor_id
        validated_data["patient_id"] = user_id
        validated_data['duration']= '__NA__'
        return super().create(validated_data)
