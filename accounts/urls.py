from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    MyTokenObtainPairView,
    RegisterPatientView,
    RegisterDoctorView,
    update_user,
    reset_password,
    forget_password,
    user_info,
)

urlpatterns = [
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/patient/", RegisterPatientView.as_view(), name="register_patient"),
    path("register/doctor/", RegisterDoctorView.as_view(), name="register_doctor"),
    path("update_user/", update_user, name="update_user"),
    path("forget_password/", forget_password, name="forget_password"),
    path("reset_password/<str:token>/", reset_password, name="reset_password"),
    path("user_info/", user_info, name="user_info"),
]
