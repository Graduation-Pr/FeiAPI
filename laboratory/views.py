# internal imports
from .models import LabBooking, Laboratory
from .filters import LaboratoryFilter
from .serializers import (
    LabBookingCancelSerializer,
    LabBookingReschdualAndCompleteSerializer,
    LabReadBookingSerializer,
    LaboratorySerializer,
    LaboratoryDetailSerializer,
)
# rest imports
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import generics
from rest_framework import status
# swagger imports
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


@swagger_auto_schema(
    method="get",
    responses={200: LaboratorySerializer(many=True)},
    operation_description="Retrieve all laboratories with pagination and filtering."
)
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_all_labs(request):
    """
    Retrieve all laboratories with pagination and filtering.
    """
    filterset = LaboratoryFilter(
        request.GET, queryset=Laboratory.objects.all().order_by("id")
    )
    paginator = PageNumberPagination()
    paginator.page_size = 6
    queryset = paginator.paginate_queryset(filterset.qs, request)

    serializer = LaboratorySerializer(queryset, many=True, context={"request": request})
    return Response({"labs": serializer.data})


class DetailLaboratory(generics.RetrieveAPIView):
    """
    Retrieve detailed information about a specific laboratory.
    """
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Laboratory.objects.all()
    serializer_class = LaboratoryDetailSerializer


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'cancel_reason': openapi.Schema(type=openapi.TYPE_STRING, description='Reason for cancellation')
        }
    ),
    responses={
        200: LabBookingCancelSerializer,
        403: 'Permission denied',
        404: 'Booking does not exist'
    },
    operation_description="Cancel a lab booking."
)
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def cancel_booking(request, pk):
    """
    Cancel a lab booking.
    """
    user = request.user
    data = request.data
    try:
        booking = LabBooking.objects.get(id=pk)
        if booking.patient == user:
            booking.is_cancelled = True
            booking.cancel_reason = data.get("cancel_reason", "")
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


@swagger_auto_schema(
    method="get",
    responses={
        200: LabReadBookingSerializer,
        403: 'Permission denied',
        404: 'Booking does not exist'
    },
    operation_description="Retrieve details of a specific lab booking."
)
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def booking_detail(request, pk):
    """
    Retrieve details of a specific lab booking.
    """
    user = request.user
    try:
        booking = LabBooking.objects.get(id=pk)
        if booking.patient == user:
            serializer = LabReadBookingSerializer(booking, context={"request":request})
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


@swagger_auto_schema(
    method="put",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'booking_date': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME, description='New booking date')
        }
    ),
    responses={
        200: LabBookingReschdualAndCompleteSerializer,
        403: 'Permission denied',
        404: 'Booking does not exist'
    },
    operation_description="Reschedule a lab booking."
)
@api_view(["PUT"])
@permission_classes([permissions.IsAuthenticated])
def reschedual_booking(request, pk):
    """
    Reschedule a lab booking.
    """
    user = request.user
    data = request.data
    new_booking_date = data.get("booking_date")
    try:
        booking = LabBooking.objects.get(id=pk)
        if booking.patient == user:
            booking.booking_date = new_booking_date
            booking.save()
            serializer = LabBookingReschdualAndCompleteSerializer(booking)
            return Response(serializer.data)
        else:
            return Response(
                {"errors": "You do not have permission to reschedule this booking."},
                status=status.HTTP_403_FORBIDDEN,
            )
    except LabBooking.DoesNotExist:
        return Response(
            {"errors": "Booking does not exist."}, status=status.HTTP_404_NOT_FOUND
        )