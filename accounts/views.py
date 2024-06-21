# internal imports
from .models import User, DoctorProfile, PatientProfile
from .serializers import (
    MyTokenObtainPairSerializer,
    RegisterDoctorSerializer,
    RegisterPatientSerializer,
    UpdateUserSerializer,
    DoctorProfileSerializer,
    PatientProfileSerializer,
)
# rest imports
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
# django imports
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
# python import
from datetime import datetime, timedelta
# swagger imports
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Custom token obtain pair view
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# Register patient view
class RegisterPatientView(generics.CreateAPIView):
    queryset = User.objects.filter(role=User.Role.PATIENT)
    permission_classes = [AllowAny]
    serializer_class = RegisterPatientSerializer

    def perform_create(self, serializer):
        serializer.save(role=User.Role.PATIENT)

# Register doctor view
class RegisterDoctorView(generics.CreateAPIView):
    queryset = User.objects.filter(role=User.Role.DOCTOR)
    permission_classes = [AllowAny]
    serializer_class = RegisterDoctorSerializer

    def perform_create(self, serializer):
        serializer.save(role=User.Role.DOCTOR)

# Update user information
@swagger_auto_schema(method='put', request_body=UpdateUserSerializer)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user

    if "password" in request.data:
        password = make_password(request.data.get("password"))
        user.set_password(password)

    user_serializer = UpdateUserSerializer(
        instance=user, data=request.data, partial=True, context={"request": request}
    )
    if user_serializer.is_valid():
        user_serializer.save()
    else:
        return Response(
            {"Error": user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    if user.role == User.Role.DOCTOR:
        profile = user.doctor_profile
        profile_serializer = DoctorProfileSerializer(
            instance=profile, data=request.data, partial=True, context={"request": request}
        )
    elif user.role == User.Role.PATIENT:
        profile = user.patient_profile
        profile_serializer = PatientProfileSerializer(
            instance=profile, data=request.data, partial=True, context={"request": request}
        )
    else:
        return Response(
            {"Error": "Invalid user role"}, status=status.HTTP_400_BAD_REQUEST
        )

    if profile_serializer.is_valid():
        profile_serializer.save()
        return Response(
            {"profile": profile_serializer.data},
            status=status.HTTP_200_OK,
        )
    else:
        return Response(
            {"Error": profile_serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

# Helper function to get current host
def get_current_host(request):
    protocol = "https" if request.is_secure() else "http"
    host = request.get_host()
    return f"{protocol}://{host}"

# Forgot password endpoint
@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL)}
))
@api_view(["POST"])
def forget_password(request):
    data = request.data
    user = get_object_or_404(User, email=data["email"])
    token = get_random_string(40)
    expire_date = datetime.now() + timedelta(minutes=30)
    user.reset_password_token = token
    user.reset_password_expire = expire_date
    user.save()
    
    return Response({"details": token})

# Reset password endpoint
@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'password': openapi.Schema(type=openapi.TYPE_STRING),
        'confirmPassword': openapi.Schema(type=openapi.TYPE_STRING)
    }
))
@api_view(["POST"])
def reset_password(request, token):
    data = request.data
    user = get_object_or_404(User, reset_password_token=token)

    if user.reset_password_expire.replace(tzinfo=None) < datetime.now():
        return Response(
            {"error": "Token is expired"}, status=status.HTTP_400_BAD_REQUEST
        )

    if data["password"] != data["confirmPassword"]:
        return Response(
            {"error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST
        )

    user.password = make_password(data["password"])
    user.reset_password_token = ""
    user.reset_password_expire = None
    user.save()
    return Response({"details": "Password reset done"})

# User information endpoint
@swagger_auto_schema(method='get', responses={200: openapi.Response('User Info', DoctorProfileSerializer)})
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_info(request):
    if request.user.role == "DOCTOR":
        doctor_profile = DoctorProfile.objects.get(user=request.user)
        serializer = DoctorProfileSerializer(doctor_profile, context={"request": request})
    else:
        patient_profile = PatientProfile.objects.get(user=request.user)
        serializer = PatientProfileSerializer(patient_profile, context={"request": request})
    return Response(serializer.data)
