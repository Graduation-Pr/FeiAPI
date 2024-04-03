from rest_framework import serializers
from accounts.models import DoctorProfile, User
from .models import DoctorBooking


class PatientBookingSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    class Meta:
        model = User
        fields = ["first_name", "last_name"]


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
    # patient = serializers.CharField(read_only=True)
    patient = PatientBookingSerializer()
    class Meta:
        model = DoctorBooking
        fields = (
            "patient",
            "service",
            "booking_day",
            "booking_hour",
            "time_ordered",
            "duration",
        )
