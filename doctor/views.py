from accounts.models import DoctorProfile, User
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status

from patient.models import PatientMedicine
from .filters import DoctorFilter
from rest_framework.pagination import PageNumberPagination
from .serializers import (
    DoctorListSerializer,
    DoctorPatientSerializer,
    DoctorReadBookingSerializer,
    DoctorBookingCancelSerializer,
    DoctorBookingReschdualAndCompleteSerializer,
    PatientMedicineCreateSerializer,
    PatientMedicineSerializer,
    PatientPlanSerializer,
    CreatePatientPlanSerializer,
)
from rest_framework.response import Response
from accounts.serializers import DoctorProfileSerializer
from .models import DoctorBooking, PatientPlan
# from .filters import DoctorBookingFilter
from django.shortcuts import get_object_or_404


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_all_docs(request):
    filterset = DoctorFilter(
        request.GET,
        queryset=DoctorProfile.objects.select_related("user").order_by("rating"),
    )
    paginator = PageNumberPagination()
    paginator.page_size = 5
    queryset = paginator.paginate_queryset(filterset.qs, request)

    serializer = DoctorListSerializer(queryset, many=True, context={"request": request})

    return paginator.get_paginated_response(serializer.data)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def doctor_detail(request, pk):
    try:
        doctor = User.objects.get(id=pk)
    except User.DoesNotExist:
        return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)

    if doctor.role == "DOCTOR":
        try:
            doctor_profile = DoctorProfile.objects.get(user=doctor)
        except DoctorProfile.DoesNotExist:
            return Response(
                {"error": "Doctor profile not found"}, status=status.HTTP_404_NOT_FOUND
            )

        doctor_bookings = DoctorBooking.objects.filter(doctor=doctor).count()
        doctor_profile.doctor_patients = doctor_bookings
        doctor_profile.save()

        serializer = DoctorProfileSerializer(doctor_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(
            {"error": "User is not a doctor"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def doctor_patients(request):
    doctor = request.user

    if doctor.role == "DOCTOR":
        bookings = DoctorBooking.objects.filter(doctor=doctor, is_cancelled=False)
        patients = set(booking.patient for booking in bookings)

        # Serialize the patients with context
        serializer = DoctorPatientSerializer(
            patients, many=True, context={"doctor": doctor}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "User is not a doctor"}, status=403)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_all_booking(request):
    queryset = DoctorBooking.objects.filter(doctor=request.user)
    # Applying the filter
    # filter = DoctorBookingFilter(request.GET, queryset=queryset)
    # queryset = filter.qs
    serializer = DoctorReadBookingSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def cancel_booking(request, pk):
    user = request.user
    data = request.data
    try:
        booking = DoctorBooking.objects.get(id=pk)
        if booking.patient == user:
            if booking.status == "completed":
                return Response("this booking is already completed", status=status.HTTP_400_BAD_REQUEST)
            if booking.status == "canceled":
                return Response("this booking is already canceled", status=status.HTTP_400_BAD_REQUEST)
            booking.cancel_reason = data.get("cancel_reason", "")
            booking.status = "canceled"  # Update the status field
            booking.save()
            serializer = DoctorBookingCancelSerializer(booking)
            return Response(serializer.data)
        else:
            return Response(
                {"errors": "You do not have permission to cancel this booking."},
                status=status.HTTP_403_FORBIDDEN,
            )
    except DoctorBooking.DoesNotExist:
        return Response(
            {"errors": "Booking does not exist."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def booking_detail(request, pk):
    user = request.user
    try:
        booking = DoctorBooking.objects.get(id=pk)
        if booking.doctor == user or booking.patient == user:
            serializer = DoctorReadBookingSerializer(booking)
            return Response(serializer.data)
        else:
            return Response(
                {"errors": "You do not have permission to view this booking."},
                status=status.HTTP_403_FORBIDDEN,
            )
    except DoctorBooking.DoesNotExist:
        return Response(
            {"errors": "Booking does not exist."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["PUT"])
@permission_classes([permissions.IsAuthenticated])
def reschedual_booking(request, pk):
    user = request.user
    data = request.data
    new_booking_date = data["booking_date"]
    try:
        booking = DoctorBooking.objects.get(id=pk)
        if booking.doctor == user or booking.patient == user:
            booking.booking_date = new_booking_date
            booking.save()
            serializer = DoctorBookingReschdualAndCompleteSerializer(booking)
            return Response(serializer.data)
        else:
            return Response(
                {"errors": "You do not have permission to reschedual this booking."},
                status=status.HTTP_403_FORBIDDEN,
            )
    except DoctorBooking.DoesNotExist:
        return Response(
            {"errors": "Booking does not exist."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["PUT"])
@permission_classes([permissions.IsAuthenticated])
def complete_booking(request, pk):
    user = request.user
    data = request.data
    try:
        booking = DoctorBooking.objects.get(id=pk)
        if booking.doctor == user:
            if booking.status == "completed":
                return Response("this booking is already completed", status=status.HTTP_400_BAD_REQUEST)
            if booking.status == "canceled":
                return Response("this booking is already canceled", status=status.HTTP_400_BAD_REQUEST)
            booking.status = "completed"
            booking.save()
            serializer = DoctorBookingReschdualAndCompleteSerializer(booking)
            return Response(serializer.data)
        else:
            return Response(
                {"errors": "You do not have permission to complete this booking."},
                status=status.HTTP_403_FORBIDDEN,
            )
    except DoctorBooking.DoesNotExist:
        return Response(
            {"errors": "Booking does not exist."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_patient_plan(request, pk):
    doctor = request.user
    patient = get_object_or_404(User, id=pk)
    if doctor.role != "DOCTOR":
        return Response(
            {"message:": "you have to be a doctor to use this function"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    if patient.role != "PATIENT":
        return Response(
            {"message:": "you have to be a user to use this function"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    patient_plan = get_object_or_404(PatientPlan, patient=patient, doctor=doctor)
    serializer = PatientPlanSerializer(patient_plan)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_patient_plan(request, pk):
    doctor = request.user
    patient = get_object_or_404(User, id=pk)
    if doctor.role != "DOCTOR":
        return Response(
            {"message:": "you have to be a doctor to use this function"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    if patient.role != "PATIENT":
        return Response(
            {"message:": "you have to be a user to use this function"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    data = {
        "doctor": doctor.id,
        "patient": patient.id,
    }

    serializer = CreatePatientPlanSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_patient_medicine(request):
    serializer = PatientMedicineCreateSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_patient_medicine(request, pk):
    patient_medicine = get_object_or_404(PatientMedicine, pk=pk)
    serializer = PatientMedicineSerializer(patient_medicine)
    return Response(serializer.data)
