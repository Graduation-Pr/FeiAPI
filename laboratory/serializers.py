from rest_framework import serializers
from .models import LabBooking, Laboratory, LabService


class LaboratorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Laboratory
        fields = ("name", "image", "rate", "city")


class LaboratoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Laboratory
        fields = "__all__"



class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabService
        fields = ('service', "price")




class LabReadBookingSerializer(serializers.ModelSerializer):
    lab = serializers.CharField(read_only=True)
    id = serializers.CharField(read_only=True)
    patient = serializers.CharField(read_only=True)
    service = ServiceSerializer()
    
    class Meta:
        model = LabBooking
        fields = (
            "id",
            "lab",
            "patient",
            "service",
            "booking_date",
        )
        
class LabBookingCancelSerializer(serializers.ModelSerializer):
    booking = LabReadBookingSerializer(read_only=True)
    lab = serializers.CharField(read_only=True)
    patient = serializers.CharField(read_only=True)
    service = serializers.CharField(read_only=True)    
    cancel_reason = serializers.CharField(required=True)
    class Meta:
        model = LabBooking
        fields = "__all__"


class LabBookingReschdualAndCompleteSerializer(serializers.ModelSerializer):
    booking = LabReadBookingSerializer(read_only=True)
    lab = serializers.CharField(read_only=True)
    patient = serializers.CharField(read_only=True)
    service = serializers.CharField(read_only=True)

    class Meta:
        model = LabBooking
        fields = "__all__"


