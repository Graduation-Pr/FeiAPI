from django.urls import path
from .views import (
    DetailLaboratory,
    reschedual_booking,
    cancel_booking,
    booking_detail,
    get_all_labs,
)

urlpatterns = [
    # Endpoint for retrieving all laboratories with pagination and filtering
    path("", get_all_labs, name="labs"),
    # Endpoint for retrieving detailed information about a specific laboratory
    path("<int:pk>/", DetailLaboratory.as_view(), name="singlelab"),
    # Endpoint for cancelling a lab booking
    path("bookings/<int:pk>/cancel/", cancel_booking, name="cancel-doctor"),
    # Endpoint for rescheduling a lab booking
    path("bookings/<int:pk>/reschedual/", reschedual_booking, name="reschedual-doctor"),
    # Endpoint for retrieving details of a specific lab booking
    path("bookings/<int:pk>/", booking_detail, name="booking-detail"),
]
