from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from .models import User, Doctor, Patient, DoctorProfile, PatientProfile
from .serializers import (
    MyTokenObtainPairSerializer,
    RegisterDoctorSerializer,
    RegisterPatientSerializer,
    DoctorProfileSerializer,
    PatientProfileSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import DoctorProfile, PatientProfile
from .serializers import DoctorProfileSerializer, PatientProfileSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterPatientView(generics.CreateAPIView):
    queryset = Patient.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterPatientSerializer

    def perform_create(self, serializer):
        serializer.save(role=User.Role.PATIENT)


class RegisterDoctorView(generics.CreateAPIView):
    queryset = Doctor.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterDoctorSerializer

    def perform_create(self, serializer):
        serializer.save(role=User.Role.DOCTOR)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_info(request):
    if request.user.role == "DOCTOR":
        doctor_profile = DoctorProfile.objects.get(user=request.user)
        serializer = DoctorProfileSerializer(doctor_profile)
    else:
        patient_profile = PatientProfile.objects.get(user=request.user)
        serializer = PatientProfileSerializer(patient_profile)
    return Response(serializer.data)
