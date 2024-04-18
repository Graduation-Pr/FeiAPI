from rest_framework import serializers
from accounts.models import DoctorProfile, User
from .models import DoctorBooking


class DoctorListSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    government = serializers.CharField(source="user.government")
    city = serializers.CharField(source="user.city")

    # Assuming 'rating' is directly on the DoctorProfile model as per your previous setup

    class Meta:
        model = DoctorProfile
        fields = ("first_name", "last_name", "government", "rating", "city")


class DoctorReadBookingSerializer(serializers.ModelSerializer):
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
            "pending_status",
        )
        
class DoctorBookingCancelSerializer(serializers.ModelSerializer):
    booking = DoctorReadBookingSerializer(read_only=True)
    cancel_reason = serializers.CharField(required=True)
    class Meta:
        model = DoctorBooking
        fields = (
            "booking",
            "is_cancelled",
            "cancel_reason",
        )



