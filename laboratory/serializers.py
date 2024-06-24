from rest_framework import serializers
from .models import LabBooking, Laboratory, LabService


class LaboratorySerializer(serializers.ModelSerializer):
    # image = serializers.SerializerMethodField()

    class Meta:
        model = Laboratory
        fields = ("id", "name", "image", "rate", "city")

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url"):
            return request.build_absolute_uri(obj.image.url)
        return None


class LaboratoryDetailSerializer(serializers.ModelSerializer):
    lab_patients = serializers.SerializerMethodField()

    class Meta:
        model = Laboratory
        fields = (
            "name",
            "image",
            "city",
            "rate",
            "phone_num",
            "technology",
            "about",
            "lab_patients",
        )

    def get_lab_patients(self, obj):
        bookings = LabBooking.objects.filter(id=obj.id).count()
        return bookings

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url"):
            return request.build_absolute_uri(obj.image.url)
        return None


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabService
        fields = ("service", "price")


class LabReadBookingSerializer(serializers.ModelSerializer):
    lab = serializers.CharField(read_only=True)
    service = serializers.CharField(source="service.service")
    image = serializers.SerializerMethodField()

    class Meta:
        model = LabBooking
        fields = (
            "id",
            "lab",
            "service",
            "status",
            "booking_date",
            "image"
        )


    def get_image(self, obj):
        request = self.context.get("request")       
        return request.build_absolute_uri(obj.lab.image.url)
    


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


class LabResultSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    lab = serializers.CharField(read_only=True)
    service = serializers.CharField()
    class Meta:
        model = LabBooking
        fields = ("id", "lab", "service", "booking_date", "image")
        

    def get_image(self, obj):
        request = self.context.get("request")       
        return request.build_absolute_uri(obj.lab.image.url)
    