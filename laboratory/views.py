from django.shortcuts import render
from .serializers import LabBookingCancelSerializer, LabBookingReschdualAndCompleteSerializer, LabReadBookingSerializer, LaboratorySerializer, LaboratoryDetailSerializer
from .models import LabBooking, Laboratory
from rest_framework import generics
from .filters import LabBookingFilter, LaboratoryFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_labs(request):
    filterset = LaboratoryFilter(
        request.GET, queryset=Laboratory.objects.all().order_by("id")
    )
    paginator = PageNumberPagination()
    paginator.page_size = 6
    queryset = paginator.paginate_queryset(filterset.qs, request)

    serializer = LaboratorySerializer(queryset, many=True)
    return Response({"labs": serializer.data})


class DetailLaboratory(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Laboratory.objects.all()
    serializer_class = LaboratoryDetailSerializer



@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_all_booking(request):
    queryset = LabBooking.objects.filter(patient=request.user)
    # Applying the filter
    filter = LabBookingFilter(request.GET, queryset=queryset)
    queryset = filter.qs
    serializer = LabReadBookingSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def cancel_booking(request, pk):
    user = request.user
    data = request.data
    try:
        booking = LabBooking.objects.get(id=pk)
        if booking.patient == user:
            booking.is_cancelled = True
            booking.cancel_reason = data["cancel_reason"]
            booking.save()
            serializer = LabBookingCancelSerializer(booking)
            return Response(serializer.data)
        else:
            return Response(
                {"errors": "You do not have permission to cancel this booking."},
                status=status.HTTP_403_FORBIDDEN,
            )
    except LabBooking.DoesNotExist:
        return Response(
            {"errors": "Booking does not exist."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def booking_detail(request, pk):
    user = request.user
    try:
        booking = LabBooking.objects.get(id=pk)
        if booking.patient == user:
            serializer = LabReadBookingSerializer(booking)
            return Response(serializer.data)
        else:
            return Response(
                {"errors": "You do not have permission to view this booking."},
                status=status.HTTP_403_FORBIDDEN,
            )
    except LabBooking.DoesNotExist:
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
        booking = LabBooking.objects.get(id=pk)
        if booking.patient == user:
            booking.booking_date = new_booking_date
            booking.save()
            serializer = LabBookingReschdualAndCompleteSerializer(booking)
            return Response(serializer.data)
        else:
            return Response(
                {"errors": "You do not have permission to reschedual this booking."},
                status=status.HTTP_403_FORBIDDEN,
            )
    except LabBooking.DoesNotExist:
        return Response(
            {"errors": "Booking does not exist."}, status=status.HTTP_404_NOT_FOUND
        )


