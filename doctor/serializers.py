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
        fields = ("first_name", "last_name", "government", "rating", "city", "image", "specialization")




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
        
        
class DoctorPatientSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    booking_id = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ("image","location","full_name","booking_id")

    def get_full_name(self, obj):
        first_name = obj.first_name
        last_name = obj.last_name
        return f"{first_name} {last_name}"
    
    def get_location(self, obj):
        city = obj.city
        government = obj.government
        return f"{government},{city}"

    def get_booking_id(self, obj):
        # Assuming you want to get the booking ID related to this doctor and patient
        doctor = self.context['doctor']
        booking = DoctorBooking.objects.filter(doctor=doctor, patient=obj).first()
        return booking.id if booking else None