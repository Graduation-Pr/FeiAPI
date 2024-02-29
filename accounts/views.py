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


# from rest_framework.permissions import IsAuthenticated
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from .serializers import DoctorProfileSerializer, PatientProfileSerializer


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


