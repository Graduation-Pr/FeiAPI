from laboratory.models import Laboratory
from .serializers import DoctorBookingSerializer, LabBookingSerializer
from orders.serializers import CreditCardSerializer
from rest_framework.response import Response
from accounts.models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import status
from doctor.models import DoctorBooking
from orders.models import CreditCard
from rest_framework.decorators import api_view, permission_classes


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_doctor_booking(request, doctor_id):
    doctor = User.objects.get(id=doctor_id)
    if doctor.role == "DOCTOR":
        data = request.data
        user = request.user
        payment_card = data["payment_card"]
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

    else:
        return Response(
            {
                "error": "Invalid Doctor ID",
                "message": "Please provide a valid Doctor ID.",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
        
        

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_lab_booking(request, lab_id):
    lab = Laboratory.objects.get(id=lab_id)
    if lab:
        data = request.data
        user = request.user
        payment_card = data["payment_card"]
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

    else:
        return Response(
            {
                "error": "Invalid Lab ID",
                "message": "Please provide a valid Lab ID.",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
