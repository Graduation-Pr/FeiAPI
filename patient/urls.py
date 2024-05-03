from django.urls import path
from .views import create_doctor_booking, create_lab_booking

urlpatterns = [
    path("doctor/<int:doctor_id>/booking/", create_doctor_booking, name="create_doctor_booking"),
    path("lab/<int:lab_id>/booking/", create_lab_booking, name="create_lab_booking"),
]