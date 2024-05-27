from doctor.models import DoctorBooking, PatientPlan
from doctor.serializers import (
    DoctorReadBookingSerializer,
    PatientMedicineSerializer,
    PatientPlanSerializer,
)
from laboratory.models import Laboratory
from .serializers import DoctorBookingSerializer, LabBookingSerializer
from rest_framework.response import Response
from accounts.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from orders.models import CreditCard
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from .models import PatientMedicine


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_doctor_booking(request, doctor_id):
    try:
        doctor = User.objects.get(id=doctor_id)
    except User.DoesNotExist:
        return Response(
            {
                "error": "Invalid Doctor ID",
                "message": "Please provide a valid Doctor ID.",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    if doctor.role != "DOCTOR":
        return Response(
            {
                "error": "Invalid Doctor ID",
                "message": "Please provide a valid Doctor ID.",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    data = request.data
    user = request.user

    try:
        payment_card = data["payment_card"]
        card = CreditCard.objects.get(id=payment_card)
        if card.user != user:
            return Response(
                {"errors": "You are not the owner of this card"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    except KeyError:
        return Response(
            {"errors": "Payment card ID is missing"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except CreditCard.DoesNotExist:
        return Response(
            {"errors": "Payment card not found"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer = DoctorBookingSerializer(
        data=data,
        context={
            "patient_id": user.id,
            "doctor_id": doctor_id,
            "payment_card": payment_card,
        },
    )

    if serializer.is_valid():
        serializer.save()
        return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)
    else:
        return Response(
            {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_lab_booking(request, lab_id):
    try:
        lab = Laboratory.objects.get(id=lab_id)
    except Laboratory.DoesNotExist:
        return Response(
            {"error": "Invalid Lab ID", "message": "Please provide a valid Lab ID."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    data = request.data
    user = request.user

    try:
        payment_card = data["payment_card"]
        card = CreditCard.objects.get(id=payment_card)
        if card.user != user:
            return Response(
                {"errors": "You are not the owner of this card"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    except KeyError:
        return Response(
            {"errors": "Payment card ID is missing"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except CreditCard.DoesNotExist:
        return Response(
            {"errors": "Payment card not found"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if not lab:
        return Response(
            {"error": "Invalid Lab ID", "message": "Please provide a valid Lab ID."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer = LabBookingSerializer(
        data=data,
        context={
            "patient_id": user.id,
            "lab_id": lab_id,
            "payment_card": payment_card,
        },
    )

    if serializer.is_valid():
        serializer.save()
        return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)
    else:
        return Response(
            {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def doctor_review(request, pk):
    if request.user.role != "PATIENT":
        return Response(
            {"message": "you have to be a patient to make review"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    patient = request.user
    data = request.data

    try:
        doctor = User.objects.get(id=pk)
    except User.DoesNotExist:
        return Response(
            {"message": "enter a valid doctor ID"}, status=status.HTTP_401_UNAUTHORIZED
        )

    if doctor.role != "DOCTOR":
        return Response(
            {"message": "enter a valid doctor ID"}, status=status.HTTP_401_UNAUTHORIZED
        )

    booking = DoctorBooking.objects.filter(
        patient=patient, doctor=doctor, is_completed=True
    ).last()

    if not booking:
        return Response(
            {
                "message": "you don't have a booking with this doctor or you have not completed your booking"
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    booking.review = data.get("review", "")
    booking.save()

    serializer = DoctorReadBookingSerializer(booking)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_patient_plans(request):
    patient = request.user
    if patient.role != "PATIENT":
        return Response(
            {"message:": "you have to be a user to use this function"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    patient_plans = PatientPlan.objects.filter(patient=patient)
    serializer = PatientPlanSerializer(patient_plans, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_patient_plan(request, pk):
    patient = request.user
    doctor = get_object_or_404(User, id=pk)
    if doctor.role != "DOCTOR":
        return Response(
            {"message:": "the id passed is not a doctor id"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    if patient.role != "PATIENT":
        return Response(
            {"message:": "you have to be a user to use this function"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    try:
        patient_plan = PatientPlan.objects.filter(doctor=doctor, patient=patient).last()
    except PatientPlan.DoesNotExist:
        return Response({"message:": "patient plan does not exist"})
    serializer = PatientPlanSerializer(patient_plan)
    return Response(serializer.data)


@api_view(["POST", "GET"])
@permission_classes([IsAuthenticated])
def take_medicine(request, pk):
    patient = request.user
    medicine = get_object_or_404(PatientMedicine, id=pk)
    if request.method == "POST":
        if patient.role != "PATIENT":
            return Response(
                {"message": "you have to be a patient to use this function"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        medicine.left -= 1
        medicine.save()
        serializer = PatientMedicineSerializer(medicine)
        return Response(serializer.data)

    if request.method == "GET":
        get_serializer = PatientMedicineSerializer(medicine)
        return Response(get_serializer.data)
