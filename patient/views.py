from django.shortcuts import render
from .serializers import DoctorWriteBookingChatAndVoiceSerializer,DoctorWriteBookingInPersonSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from accounts.models import DoctorProfile
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action


class DoctorBooking(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = DoctorWriteBookingChatAndVoiceSerializer

    @action(detail=True, methods=["POST"])
    def doctor_booking_chat_and_voice(self, request, pk):
        doctor = DoctorProfile.objects.get(id=pk)
        serializer = DoctorWriteBookingChatAndVoiceSerializer(
            data=request.data, context={"user_id": request.user.id, "doctor_id": pk}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    @action(detail=True, methods=["POST"])
    def doctor_booking_inperson(self, request, pk):
        doctor = DoctorProfile.objects.get(id=pk)
        serializer = DoctorWriteBookingInPersonSerializer(
            data=request.data, context={"user_id": request.user.id, "doctor_id": pk}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
