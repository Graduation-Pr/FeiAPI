from django.urls import path
from .views import (
    MyTokenObtainPairView,
    RegisterPatientView,
    RegisterDoctorView,
    user_info,
)

urlpatterns = [
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("register/patient/", RegisterPatientView.as_view(), name="register_patient"),
    path("register/doctor/", RegisterDoctorView.as_view(), name="register_doctor"),
    path("user_info/", user_info),
]
