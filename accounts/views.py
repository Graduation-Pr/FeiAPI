from .models import User
from .serializers import (
    MyTokenObtainPairSerializer,
    RegisterDoctorSerializer,
    RegisterPatientSerializer,
    UserSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from datetime import datetime, timedelta


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterPatientView(generics.CreateAPIView):
    queryset = User.objects.filter(role=User.Role.PATIENT)
    permission_classes = [AllowAny]
    serializer_class = RegisterPatientSerializer

    def perform_create(self, serializer):
        serializer.save(role=User.Role.PATIENT)


class RegisterDoctorView(generics.CreateAPIView):
    queryset = User.objects.filter(role=User.Role.DOCTOR)
    permission_classes = [AllowAny]
    serializer_class = RegisterDoctorSerializer

    def perform_create(self, serializer):
        serializer.save(role=User.Role.DOCTOR)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user

    if "password" in request.data:
        password = make_password(request.data.get("password"))
        user.set_password(password)

    serializer = UserSerializer(instance=user, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(
            {"Error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


def get_current_host(request):
    protocol = request.is_secure() and "https" or "http"
    host = request.get_host()

    return f"{protocol}//{host}"


@api_view(["POST"])
def forget_password(request):
    data = request.data
    user = get_object_or_404(User, email=data["email"])
    token = get_random_string(40)
    expire_date = datetime.now() + timedelta(minutes=30)
    user.reset_password_token = token
    user.reset_password_expire = expire_date
    user.save()

    # host = get_current_host(request)
    link = "http://localhost:8000/reset_password/{token}".format(token=token)
    body = "Your password reset link is : {link}".format(link=link)
    send_mail("Paswword reset from Fie", body, "Fie@gmail.com", [data["email"]])
    return Response(
        {"details": "Password reset sent to {email}".format(email=data["email"])}
    )


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
            {"error": "Password are not same"}, status=status.HTTP_400_BAD_REQUEST
        )

    user.password = make_password(data["password"])
    user.reset_password_token = ""
    user.reset_password_expire = None
    user.save()
    return Response({"details": "Password reset done "})
