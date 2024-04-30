from django.shortcuts import render
from accounts.models import DoctorProfile, User
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from .filters import DoctorFilter
from rest_framework.pagination import PageNumberPagination
from .serializers import (
    DoctorListSerializer,
    DoctorReadBookingSerializer,
    DoctorBookingCancelSerializer,
    DoctorBookingReschdualAndCompleteSerializer,
)
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import DoctorProfileSerializer
from .models import DoctorBooking
from .filters import DoctorBookingFilter


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

    serializer = DoctorListSerializer(queryset, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(["GET"])
def doctor_detail(request, pk):
    doctor = User.objects.get(id=pk)
    if doctor.role == "DOCTOR":
        doctor_profile = DoctorProfile.objects.get(user=doctor)
        doctor_bookings = DoctorBooking.objects.filter(doctor=doctor).count()
        doctor_profile.doctor_patients = doctor_bookings
        doctor_profile.save()

        serializer = DoctorProfileSerializer(doctor_profile)
        return Response(serializer.data)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_all_booking(request):
    queryset = DoctorBooking.objects.filter(doctor=request.user)
    # Applying the filter
    filter = DoctorBookingFilter(request.GET, queryset=queryset)
    queryset = filter.qs
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
            booking.is_cancelled = True
            booking.cancel_reason = data["cancel_reason"]
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
            booking.is_completed = True
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
