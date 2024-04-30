from django.urls import path
from .views import create_doctor_booking

urlpatterns = [
    path("doctor/<int:doctor_id>/booking/", create_doctor_booking, name="create_doctor_booking"),
]