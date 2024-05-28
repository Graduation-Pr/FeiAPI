from rest_framework import serializers
from accounts.models import DoctorProfile, User
from accounts.serializers import SimpleUserSerializer
from .models import DoctorBooking, Service, PatientPlan
from patient.models import PatientMedicine
from pharmacy.serializers import SimpleMedicineSerializer


class DoctorListSerializer(serializers.ModelSerializer):
    doctor_id = serializers.SerializerMethodField()
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    government = serializers.CharField(source="user.government")
    city = serializers.CharField(source="user.city")
    image = serializers.ImageField(source="user.image", read_only=True)

    class Meta:
        model = DoctorProfile
        fields = (
            "doctor_id",
            "first_name",
            "last_name",
            "government",
            "rating",
            "city",
            "image",
            "specialization",
        )

    def get_doctor_id(self, obj):
        return obj.user.id


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ("service", "price")


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
            "status",
            "review",
            "rating",
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
        fields = ("image", "location", "full_name", "booking_id")

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
        doctor = self.context["doctor"]
        booking = DoctorBooking.objects.filter(doctor=doctor, patient=obj).last()
        return booking.id if booking else None


class PatientMedicineSerializer(serializers.ModelSerializer):
    medicine = SimpleMedicineSerializer()

    class Meta:
        model = PatientMedicine
        fields = (
            "id",
            "medicine",
            "dose",
            "program",
            "plan",
            "quantity",
            "left",
            "start_date",
            "end_date",
        )


class PatientPlanSerializer(serializers.ModelSerializer):
    patient_medicines = PatientMedicineSerializer(source="medicine_plan", many=True)
    doctor = SimpleUserSerializer(read_only=True)
    patient = SimpleUserSerializer(read_only=True)

    class Meta:
        model = PatientPlan
        fields = ("id", "doctor", "patient", "patient_medicines")


class CreatePatientPlanSerializer(serializers.ModelSerializer):
    patient_medicines = PatientMedicineSerializer(
        source="medicine_plan", many=True, read_only=True, required=False
    )

    class Meta:
        model = PatientPlan
        fields = ("id", "doctor", "patient", "patient_medicines")


class PatientMedicineCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientMedicine
        fields = ("medicine", "dose", "program", "plan")

    def create(self, validated_data):
        patient_medicine = PatientMedicine.objects.create(**validated_data)
        return patient_medicine
