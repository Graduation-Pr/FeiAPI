# internal imports
from doctor.serializers import SimplePatientPlanMedicineSerializer
from doctor.models import DoctorBooking, PatientPlan
from laboratory.models import LabBooking
from orders.models import CreditCard
from accounts.models import User
# rest import
from rest_framework import serializers


class DoctorBookingSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and retrieving doctor bookings.
    """
    doctor = serializers.CharField(read_only=True, source="doctor.full_name")
    patient = serializers.CharField(read_only=True, source="patient.full_name")
    payment_card = serializers.CharField(read_only=True)
    service_price = serializers.SerializerMethodField()
    patient_plan = serializers.SerializerMethodField()

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
            "patient_plan",
        ]

    def get_service_price(self, obj):
        """
        Method to get the price of the service.
        """
        return obj.service.price

    def create(self, validated_data):
        """
        Custom create method to handle additional context data.
        """
        print("Context in Serializer:", self.context)
        patient_id = self.context["patient_id"]
        doctor_id = self.context["doctor_id"]
        payment_card_id = self.context["payment_card"]

        card = CreditCard.objects.get(id=payment_card_id)

        validated_data["doctor_id"] = doctor_id
        validated_data["patient_id"] = patient_id
        validated_data["payment_card"] = card
        return super().create(validated_data)

    def get_patient_plan(self, obj):
        """
        Method to create and get the patient plan ID.
        """
        patient_id = self.context["patient_id"]
        doctor_id = self.context["doctor_id"]
        patient = User.objects.get(id=patient_id)
        doctor = User.objects.get(id=doctor_id)
        patient_plan = PatientPlan.objects.create(doctor=doctor, patient=patient)
        return patient_plan.id


class LabBookingSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and retrieving lab bookings.
    """
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
        """
        Custom create method to handle additional context data.
        """
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
        """
        Method to get the price of the service.
        """
        return obj.service.price


class PatientReadBookingSerializer(serializers.ModelSerializer):
    """
    Serializer for reading doctor bookings with minimal details for patients.
    """
    doctor = serializers.CharField(read_only=True, source="doctor.full_name")
    id = serializers.CharField(read_only=True)
    service = serializers.CharField(source='service.service')
    doctor_image = serializers.SerializerMethodField()

    class Meta:
        model = DoctorBooking
        fields = (
            "id",
            "doctor",
            "service",
            "booking_date",
            "status",
            "doctor_image"
        )

    def get_doctor_image(self, obj):
        """
        Method to get the full URL of the doctor's image.
        """
        request = self.context.get("request")
        if obj.doctor.image and hasattr(obj.doctor.image, "url"):
            return request.build_absolute_uri(obj.doctor.image.url)
        return None


class PatientReadBookingDetailsSerializer(serializers.ModelSerializer):
    """
    Serializer for reading detailed doctor bookings for patients.
    """
    doctor = serializers.CharField(read_only=True, source="doctor.full_name")
    id = serializers.CharField(read_only=True)
    service = serializers.CharField(source='service.service')
    doctor_image = serializers.SerializerMethodField()
    payment_card = serializers.CharField()
    price = serializers.CharField(source="service.price")

    class Meta:
        model = DoctorBooking
        fields = (
            "id",
            "doctor",
            "service",
            "payment_card",
            "booking_date",
            "status",
            "doctor_image",
            "price"
        )

    def get_doctor_image(self, obj):
        """
        Method to get the full URL of the doctor's image.
        """
        request = self.context.get("request")
        if obj.doctor.image and hasattr(obj.doctor.image, "url"):
            return request.build_absolute_uri(obj.doctor.image.url)
        return None


class DoctorPlanSerializer(serializers.ModelSerializer):
    """
    Serializer for reading doctor plans.
    """
    doctor = serializers.CharField(read_only=True, source="doctor.full_name")
    sepcializtion = serializers.CharField(
        read_only=True, source="doctor.doctor_profile.specialization"
    )
    rating = serializers.CharField(
        read_only=True, source="doctor.doctor_profile.rating"
    )
    image = serializers.SerializerMethodField()

    class Meta:
        model = PatientPlan
        fields = ("id", "doctor", "sepcializtion", "rating", "image")

    def get_image(self, obj):
        """
        Method to get the full URL of the doctor's image.
        """
        request = self.context.get("request")
        if obj.doctor.image and hasattr(obj.doctor.image, "url"):
            return request.build_absolute_uri(obj.doctor.image.url)
        return None


class DoctorPatientPlanDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed view of doctor plans with associated patient medicines.
    """
    patient_medicines = SimplePatientPlanMedicineSerializer(source="medicine_plan", many=True)
    doctor = serializers.CharField(read_only=True, source="doctor.full_name")
    image = serializers.SerializerMethodField()

    class Meta:
        model = PatientPlan
        fields = ("id", "doctor", "image", "patient_medicines")

    def get_image(self, obj):
        """
        Method to get the full URL of the patient's image.
        """
        request = self.context.get("request")
        if obj.patient.image and hasattr(obj.patient.image, "url"):
            return request.build_absolute_uri(obj.patient.image.url)
        return None