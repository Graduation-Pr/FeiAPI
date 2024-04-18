from .serializers import DoctorWriteBookingSerializer, BookingOrderSerializer
from orders.serializers import CreditCardSerializer
from rest_framework.response import Response
from accounts.models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import status
from doctor.models import DoctorBooking
from orders.models import CreditCard


class DoctorBookingViewSet(ModelViewSet):
    queryset = DoctorBooking.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = BookingOrderSerializer

    @action(detail=True, methods=["POST"])
    def doctor_booking(self, request, pk):
        user = User.objects.get(id=pk)
        data = request.data
        if user.role == "DOCTOR":
            serializer = DoctorWriteBookingSerializer(
                data=request.data, context={"user_id": request.user.id, "doctor_id": pk}
            )
            card_id = data.get("card_id")
            try:   
                card = CreditCard.objects.get(id=card_id)
            except CreditCard.DoesNotExist:
                return Response({"error": "Card not found"}, status=status.HTTP_404_NOT_FOUND)
            
            if serializer.is_valid():
                booking_instance = serializer.save(payment_card=card)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"error": "Invalid Doctor ID", "message": "Please provide a valid Doctor ID."},
                status=status.HTTP_400_BAD_REQUEST
            )

