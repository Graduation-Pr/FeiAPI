from django.urls import path
from .views import DoctorBooking

urlpatterns = [
    path('doctor/<int:pk>/booking/', DoctorBooking.as_view({'post': 'doctor_booking'}), name='create_doctor_booking'),
]
