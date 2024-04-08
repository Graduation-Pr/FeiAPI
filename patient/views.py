from django.shortcuts import render
from .serializers import DoctorWriteBookingSerializer, BookingOrderSerializer, CreditCardSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from accounts.models import User
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import status
from doctor.models import DoctorBooking, CreditCard

class DoctorBookingViewSet(ModelViewSet):
    queryset = DoctorBooking.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = BookingOrderSerializer

    @action(detail=True, methods=["POST"])
    def doctor_booking(self, request, pk):
        user = User.objects.get(id=pk)
        if user.role == "DOCTOR":
            serializer = DoctorWriteBookingSerializer(
                data=request.data, context={"user_id": request.user.id, "doctor_id": pk}
            )
            serializer.is_valid(raise_exception=True)
            booking_instance = serializer.save()

            credit_card_data = request.data.get('payment_card', None)
            if credit_card_data:
                credit_card_serializer = CreditCardSerializer(data=credit_card_data)
                if credit_card_serializer.is_valid():
                    # Assuming the credit card is saved in the database
                    credit_card = credit_card_serializer.save(user=request.user)
                    # Update the booking instance with payment status and associated credit card
                    booking_instance.payment_status = DoctorBooking.PAYMENT_STATUS_COMPLETE
                    booking_instance.payment_card = credit_card
                    booking_instance.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(credit_card_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # If no credit card details provided, mark the booking as pending payment
            booking_instance.payment_status = DoctorBooking.PAYMENT_STATUS_PENDING
            booking_instance.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(
            {"error": "Invalid Doctor ID", "message": "Please provide a valid Doctor ID."},
            status=status.HTTP_400_BAD_REQUEST
        )
