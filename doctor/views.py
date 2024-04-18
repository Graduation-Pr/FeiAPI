from django.shortcuts import render
from accounts.models import DoctorProfile, User
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from .filters import DoctorFilter
from rest_framework.pagination import PageNumberPagination
from .serializers import DoctorListSerializer, DoctorReadBookingSerializer, DoctorBookingCancelSerializer
from rest_framework.response import Response
from rest_framework import  status
from accounts.serializers import DoctorProfileSerializer
from .models import DoctorBooking


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_all_docs(request):
    # Assuming DoctorProfileFilter is adjusted to work with DoctorProfile instances
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
    queryset = DoctorProfile.objects.get(id=pk)
    serializer = DoctorProfileSerializer(queryset)
    return Response(serializer.data)



@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_all_booking(request):
    queryset = DoctorBooking.objects.filter(doctor=request.user)
    serializer = DoctorReadBookingSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def cancel_booking(request, pk):
    user = request.user
    try:
        booking = DoctorBooking.objects.get(id=pk)
        if booking.doctor == user or booking.patient == user:
            booking.is_cancelled = True
            booking.save()
            serializer = DoctorBookingCancelSerializer(booking)
            return Response(serializer.data)
        else:
            return Response({"errors": "You do not have permission to cancel this booking."},
                            status=status.HTTP_403_FORBIDDEN)
    except DoctorBooking.DoesNotExist:
        return Response({"errors": "Booking does not exist."},
                        status=status.HTTP_404_NOT_FOUND)
        


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def booking_detail(request,pk):
    user = request.user
    try:
        booking = DoctorBooking.objects.get(id=pk)
        if booking.doctor == user or booking.patient == user:
            serializer = DoctorReadBookingSerializer(booking)
            return Response(serializer.data)
        else:
            return Response({"errors": "You do not have permission to view this booking."},
                            status=status.HTTP_403_FORBIDDEN)
    except DoctorBooking.DoesNotExist:
        return Response({"errors": "Booking does not exist."},
                        status=status.HTTP_404_NOT_FOUND)