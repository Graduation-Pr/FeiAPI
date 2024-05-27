from django.urls import path
from .views import (
    cancel_booking,
    create_doctor_booking,
    create_lab_booking,
    doctor_review,
    get_patient_plans,
    get_patient_plan,
    take_medicine,
    get_all_bookings,
)

urlpatterns = [
    path(
        "doctor/<int:doctor_id>/booking/",
        create_doctor_booking,
        name="create_doctor_booking",
    ),
    path("lab/<int:lab_id>/booking/", create_lab_booking, name="create_lab_booking"),
    path("doctor/<int:pk>/review/", doctor_review),
    path("plans/", get_patient_plans),
    path("plans/<int:pk>/", get_patient_plan),
    path("take_medicine/<int:pk>/", take_medicine),
    path("bookings/", get_all_bookings, name="booking"),
    path("bookings/<int:pk>/cancel/", cancel_booking, name="cancel-doctor"),
]
