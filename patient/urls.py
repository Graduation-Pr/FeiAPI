from django.urls import path
from .views import (
    cancel_booking,
    create_doctor_booking,
    create_lab_booking,
    doctor_review,
    get_patient_plans,
    get_patient_plan,
    take_medicine,
    get_doctor_bookings,
    get_lab_bookings,
    list_doctor_tests,
    list_doctor_question
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
    path("doctor_bookings/", get_doctor_bookings, name="booking"),
    path("lab_bookings/", get_lab_bookings, name="booking"),
    path("doctor_bookings/<int:pk>/cancel/", cancel_booking, name="cancel-doctor"),
    path("doctor_tests/<int:pk>/", list_doctor_tests),
    path("doctor_questions/<int:pk>/", list_doctor_question)
]
