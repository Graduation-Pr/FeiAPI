from .models import LabBooking, Laboratory, LabService
from rest_framework import serializers


class LaboratorySerializer(serializers.ModelSerializer):
    """
    Serializer for Laboratory model with basic details.
    """

    class Meta:
        model = Laboratory
        fields = ("id", "name", "image", "rate", "city")

    def get_image(self, obj):
        """
        Method to get the absolute URL of the laboratory image.
        """
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url"):
            return request.build_absolute_uri(obj.image.url)
        return None


class LaboratoryDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed view of Laboratory model.
    """
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
        """
        Method to get the count of patients associated with the laboratory.
        """
        bookings = LabBooking.objects.filter(lab=obj).count()
        return bookings

    def get_image_url(self, obj):
        """
        Method to get the absolute URL of the laboratory image.
        """
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url"):
            return request.build_absolute_uri(obj.image.url)
        return None


class ServiceSerializer(serializers.ModelSerializer):
    """
    Serializer for LabService model.
    """
    class Meta:
        model = LabService
        fields = ("service", "price")


class LabReadBookingSerializer(serializers.ModelSerializer):
    """
    Serializer for reading LabBooking details.
    """
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
        """
        Method to get the absolute URL of the laboratory image associated with the booking.
        """
        request = self.context.get("request")
        return request.build_absolute_uri(obj.lab.image.url)


class LabBookingCancelSerializer(serializers.ModelSerializer):
    """
    Serializer for cancelling a LabBooking.
    """
    booking = LabReadBookingSerializer(read_only=True)
    lab = serializers.CharField(read_only=True)
    patient = serializers.CharField(read_only=True)
    service = serializers.CharField(read_only=True)
    cancel_reason = serializers.CharField(required=True)

    class Meta:
        model = LabBooking
        fields = "__all__"


class LabBookingReschdualAndCompleteSerializer(serializers.ModelSerializer):
    """
    Serializer for rescheduling and completing a LabBooking.
    """
    booking = LabReadBookingSerializer(read_only=True)
    lab = serializers.CharField(read_only=True)
    patient = serializers.CharField(read_only=True)
    service = serializers.CharField(read_only=True)

    class Meta:
        model = LabBooking
        fields = "__all__"


class LabResultSerializer(serializers.ModelSerializer):
    """
    Serializer for lab results associated with a LabBooking.
    """
    image = serializers.SerializerMethodField()
    lab = serializers.CharField(read_only=True)
    service = serializers.CharField()

    class Meta:
        model = LabBooking
        fields = ("id", "lab", "service", "booking_date", "image")

    def get_image(self, obj):
        """
        Method to get the absolute URL of the laboratory image associated with the lab result.
        """
        request = self.context.get("request")
        return request.build_absolute_uri(obj.lab.image.url)
