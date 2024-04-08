from django.urls import path
from .views import DoctorBookingViewSet

urlpatterns = [
    path("doctor/<int:pk>/booking/", DoctorBookingViewSet.as_view({"post": "doctor_booking"}), name="create_doctor_booking"),
]