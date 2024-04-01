from rest_framework import serializers
from accounts.models import DoctorProfile
from doctor.models import DoctorBooking


class DoctorWriteBookingSerializer(serializers.ModelSerializer):
    doctor = serializers.CharField(read_only=True)
    id = serializers.CharField(read_only=True)
    class Meta:
        model = DoctorBooking
        fields = ("id", "service", "booking_day", "booking_hour", "time_ordered", "duration", "doctor")

    def create(self, validated_data):
        user_id = self.context["user_id"]
        doctor_id = self.context["doctor_id"]
        validated_data["doctor_id"] = doctor_id  
        validated_data["patient_id"] = user_id    
        return super().create(validated_data)