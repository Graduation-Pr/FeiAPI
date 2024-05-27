from django.urls import path
from .views import (get_all_labs, DetailLaboratory, 
                    cancel_booking, reschedual_booking,booking_detail) 


urlpatterns = [
    path("", get_all_labs, name="labs"),
    path("<int:pk>/", DetailLaboratory.as_view(), name="singlelab"),
    # path("bookings/", get_all_booking, name="booking"),
    path("bookings/<int:pk>/cancel/", cancel_booking, name="cancel-doctor"),
    path("bookings/<int:pk>/reschedual/", reschedual_booking, name="reschedual-doctor"),
    path("bookings/<int:pk>/", booking_detail, name="booking-detail"),
]
