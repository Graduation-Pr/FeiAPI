from django.shortcuts import render
from .serializers import DoctorWriteBookingSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from accounts.models import DoctorProfile
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action


class DoctorBooking(ModelViewSet):
    permission_classes = [IsAuthenticated]  
    serializer_class = DoctorWriteBookingSerializer
    
    @action(detail=True, methods=["POST"])
    def doctor_booking(self,request,pk):
        doctor = DoctorProfile.objects.get(id=pk)
        serializer = DoctorWriteBookingSerializer(data=request.data, context={"user_id": request.user.id, "doctor_id": pk})  
        serializer.is_valid(raise_exception=True)  
        serializer.save()  
        return Response(serializer.data)