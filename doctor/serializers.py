from rest_framework import serializers
from accounts.models import DoctorProfile, User
from .models import DoctorBooking, Service


class DoctorListSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    government = serializers.CharField(source="user.government")
    city = serializers.CharField(source="user.city")
    image = serializers.CharField(source="user.image")

    class Meta:
        model = DoctorProfile
        fields = ("first_name", "last_name", "government", "rating", "city", "image")




class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('service', "price")




class DoctorReadBookingSerializer(serializers.ModelSerializer):
    doctor = serializers.CharField(read_only=True)
    id = serializers.CharField(read_only=True)
    patient = serializers.CharField(read_only=True)
    service = ServiceSerializer()
    
    class Meta:
        model = DoctorBooking
        fields = (
            "id",
            "doctor",
            "patient",
            "service",
            "booking_date",
        )
        
class DoctorBookingCancelSerializer(serializers.ModelSerializer):
    booking = DoctorReadBookingSerializer(read_only=True)
    doctor = serializers.CharField(read_only=True)
    patient = serializers.CharField(read_only=True)
    service = serializers.CharField(read_only=True)    
    cancel_reason = serializers.CharField(required=True)
    class Meta:
        model = DoctorBooking
        fields = "__all__"


class DoctorBookingReschdualAndCompleteSerializer(serializers.ModelSerializer):
    booking = DoctorReadBookingSerializer(read_only=True)
    doctor = serializers.CharField(read_only=True)
    patient = serializers.CharField(read_only=True)
    service = serializers.CharField(read_only=True)

    class Meta:
        model = DoctorBooking
        fields = "__all__"


