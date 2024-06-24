# internal imports
from orders.serializers import CreditCardSerializer
from .models import DoctorBooking, Prescription, Service, PatientPlan, DoctorComment
from patient.models import PatientMedicine, Test, Question
from pharmacy.serializers import SimpleMedicineSerializer
from accounts.serializers import SimpleUserSerializer
from accounts.models import DoctorProfile, User
# rest imports
from rest_framework import serializers


# Serializer for DoctorProfile model to show doctor details
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

# Serializer for Service model
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ("service", "price")

# Serializer for reading booking details
class DoctorReadBookingSerializer(serializers.ModelSerializer):
    doctor = serializers.CharField(read_only=True)
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
        request = self.context.get("request")
        if obj.doctor.image and hasattr(obj.doctor.image, "url"):
            return request.build_absolute_uri(obj.doctor.image.url)
        return None
    


class DoctorReadBookingDetailsSerializer(serializers.ModelSerializer):
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
        request = self.context.get("request")
        if obj.doctor.image and hasattr(obj.doctor.image, "url"):
            return request.build_absolute_uri(obj.doctor.image.url)
        return None


# Serializer for canceling a booking
class DoctorBookingCancelSerializer(serializers.ModelSerializer):
    booking = DoctorReadBookingSerializer(read_only=True)
    doctor = serializers.CharField(read_only=True)
    patient = serializers.CharField(read_only=True)
    service = serializers.CharField(read_only=True)
    cancel_reason = serializers.CharField(required=True)

    class Meta:
        model = DoctorBooking
        fields = "__all__"

# Serializer for rescheduling and completing a booking
class DoctorBookingReschdualAndCompleteSerializer(serializers.ModelSerializer):
    booking = DoctorReadBookingSerializer(read_only=True)
    doctor = serializers.CharField(read_only=True)
    patient = serializers.CharField(read_only=True)
    service = serializers.CharField(read_only=True)

    class Meta:
        model = DoctorBooking
        fields = "__all__"

# Serializer for patient details related to a specific doctor
class DoctorPatientSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    booking_id = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ("id", "image_url", "location", "full_name", "booking_id")

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def get_location(self, obj):
        return f"{obj.government},{obj.city}"

    def get_booking_id(self, obj):
        # Assuming you want to get the booking ID related to this doctor and patient
        doctor = self.context["doctor"]
        booking = DoctorBooking.objects.filter(doctor=doctor, patient=obj).last()
        return booking.id if booking else None

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url"):
            return request.build_absolute_uri(obj.image.url)
        return None

# Serializer for patient medicine details
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

# Simplified serializer for patient medicine details
class SimplePatientMedicineSerializer(serializers.ModelSerializer):
    medicine = SimpleMedicineSerializer()

    class Meta:
        model = PatientMedicine
        fields = (
            "id",
            "medicine",
            "dose",
            "quantity",
        )

# Serializer for patient plan details
class PatientPlanSerializer(serializers.ModelSerializer):
    patient_medicines = PatientMedicineSerializer(source="medicine_plan", many=True)
    doctor = SimpleUserSerializer(read_only=True)
    patient = SimpleUserSerializer(read_only=True)

    class Meta:
        model = PatientPlan
        fields = ("id", "doctor", "patient", "patient_medicines")

# Serializer for creating a patient plan
class CreatePatientPlanSerializer(serializers.ModelSerializer):
    patient_medicines = PatientMedicineSerializer(
        source="medicine_plan", many=True, read_only=True, required=False
    )

    class Meta:
        model = PatientPlan
        fields = ("id", "doctor", "patient", "patient_medicines")

# Serializer for creating a patient medicine entry
class PatientMedicineCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientMedicine
        fields = ("medicine", "dose", "program", "plan")

    def create(self, validated_data):
        return PatientMedicine.objects.create(**validated_data)

# Serializer for doctor reviews
class DoctorReviewsSerializer(serializers.ModelSerializer):
    patient = serializers.SerializerMethodField()

    class Meta:
        model = DoctorBooking
        fields = ('patient', 'review', "rating")

    def get_patient(self, obj):
        return obj.patient.full_name

# Serializer for doctor comments
class DoctorCommentSerializer(serializers.ModelSerializer):
    booking = serializers.CharField(read_only=True)

    class Meta:
        model = DoctorComment
        fields = ("text", "booking")

    def create(self, validated_data):
        return DoctorComment.objects.create(**validated_data)

# Serializer for questions related to tests
class QuestionSerializer(serializers.ModelSerializer):
    answer = serializers.CharField(read_only=True)
    test = serializers.CharField(read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'answer', 'test']

# Serializer for tests
class TestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    date = serializers.CharField(read_only=True)
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Test
        fields = ['id', 'date', 'booking', 'questions', 'image_url', 'name']

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.booking.patient.image and hasattr(obj.booking.patient.image, "url"):
            return request.build_absolute_uri(obj.booking.patient.image.url)
        return None

# Serializer for prescriptions
class PrescriptionSerializer(serializers.ModelSerializer):
    doctor = serializers.CharField(source="patient_plan.doctor.username")
    specialization = serializers.CharField(source="patient_plan.doctor.doctor_profile.specialization")
    doctor_phone_num = serializers.CharField(source="patient_plan.doctor.phone_number")
    patient = serializers.CharField(source="patient_plan.patient.username")
    patient_medicines = serializers.SerializerMethodField()

    class Meta:
        model = Prescription
        fields = (
            "id",
            "date",
            "doctor",
            "doctor_phone_num",
            "specialization",
            "patient",
            "patient_medicines"
        )

    def get_patient_medicines(self, obj):
        patient_medicines = PatientMedicine.objects.filter(plan=obj.patient_plan)
        return SimplePatientMedicineSerializer(patient_medicines, many=True).data

# Simplified serializer for doctor prescriptions
class SimpleDocPrescriptionSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    full_name = serializers.CharField(source="patient_plan.patient.full_name")

    class Meta:
        model = Prescription
        fields = ("id", "date", "image_url", "full_name")

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.patient_plan.patient.image and hasattr(obj.patient_plan.patient.image, "url"):
            return request.build_absolute_uri(obj.patient_plan.patient.image.url)
        return None

# Simplified serializer for patient prescriptions
class SimplePatientPrescriptionSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    full_name = serializers.CharField(source="patient_plan.doctor.full_name")

    class Meta:
        model = Prescription
        fields = ("id", "date", "image_url", "full_name")

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.patient_plan.patient.image and hasattr(obj.patient_plan.patient.image, "url"):
            return request.build_absolute_uri(obj.patient_plan.patient.image.url)
        return None