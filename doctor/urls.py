from django.urls import path
from .views import get_all_docs, doctor_detail, get_all_booking

urlpatterns = [
    path("", get_all_docs, name="doctor-list"),
    path("<int:pk>/", doctor_detail, name="doctor"),
    path("bookings/", get_all_booking , name="booking"),
    
]
