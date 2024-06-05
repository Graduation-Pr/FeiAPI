from django.urls import path
from .views import (
    get_all_docs,
    doctor_detail,
    get_all_bookings,
    booking_detail,
    reschedual_booking,
    complete_booking,
    doctor_patients,
    get_patient_plan,
    create_patient_plan,
    create_patient_medicine,
    get_patient_medicine,
    get_doctor_reviews,
    doctor_comment,
)

urlpatterns = [
    path("", get_all_docs, name="doctor-list"),
    path("<int:pk>/", doctor_detail, name="doctor"),
    path("bookings/", get_all_bookings, name="booking"),
    path("reviews/", get_doctor_reviews, name="reviews"),
    path("bookings/<int:pk>/reschedual/", reschedual_booking, name="reschedual-doctor"),
    path("bookings/<int:pk>/complete/", complete_booking, name="reschedual-doctor"),
    path("bookings/<int:pk>/", booking_detail, name="booking-detail"),
    path("patients/", doctor_patients, name="doctor-patients"),
    path("patient_plan/<int:pk>/", get_patient_plan),
    path("create/patient_plan/<int:pk>/", create_patient_plan),
    path(
        "create/patient_medicine/",
        create_patient_medicine,
        name="create_patient_medicine",
    ),
    path(
        "patient_medicine/<int:pk>/", get_patient_medicine, name="get_patient_medicine"
    ),
    path("comment/<int:pk>/", doctor_comment)
]
