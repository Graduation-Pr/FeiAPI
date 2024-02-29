from django.urls import path
from .views import (
    MyTokenObtainPairView,
    RegisterPatientView,
    RegisterDoctorView,
    update_user,
    reset_password,
    forget_password
    
)

urlpatterns = [
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("register/patient/", RegisterPatientView.as_view(), name="register_patient"),
    path("register/doctor/", RegisterDoctorView.as_view(), name="register_doctor"),
    path("update_user/", update_user),
    path('forget_password/', forget_password ),
    path('reset_password/<str:token>/',reset_password)
]
