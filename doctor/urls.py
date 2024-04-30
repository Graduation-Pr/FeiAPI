from django.urls import path
from .views import (
    get_all_docs,
    doctor_detail,
    get_all_booking,
    cancel_booking,
    booking_detail,
    reschedual_booking,
    complete_booking,
)

urlpatterns = [
    path("", get_all_docs, name="doctor-list"),
    path("<int:pk>/", doctor_detail, name="doctor"),
    path("bookings/", get_all_booking, name="booking"),
    path("bookings/<int:pk>/cancel/", cancel_booking, name="cancel-doctor"),
    path("bookings/<int:pk>/reschedual/", reschedual_booking, name="reschedual-doctor"),
    path("bookings/<int:pk>/complete/", complete_booking, name="reschedual-doctor"),
    path("bookings/<int:pk>/", booking_detail, name="booking-detail"),
]
