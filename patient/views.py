from django.shortcuts import render
from .serializers import DoctorWriteBookingSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from accounts.models import User
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import status

class DoctorBooking(ModelViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["POST"])
    def doctor_booking(self, request, pk):
        user = User.objects.get(id=pk)
        if user.role =="DOCTOR":            
            serializer = DoctorWriteBookingSerializer(
                data=request.data, context={"user_id": request.user.id, "doctor_id": pk}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        return Response({"error": "Invalid Doctor ID", "message": "Please provide a valid Doctor ID."}, status=status.HTTP_400_BAD_REQUEST)