from django.urls import path
from .views import DoctorBooking

urlpatterns = [
    path("doctor/<int:pk>/booking/voice&chat/", DoctorBooking.as_view({"post": "doctor_booking_chat_and_voice"}),name="create_doctor_booking_chat_and_voice",),
    path("doctor/<int:pk>/booking/inperson/", DoctorBooking.as_view({"post": "doctor_booking_inperson"}),name="create_doctor_booking_inperson",),
]
