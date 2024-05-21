from django.urls import path
from .views import create_doctor_booking, create_lab_booking, doctor_review, get_patient_plans, get_patient_plan, take_medicine

urlpatterns = [
    path("doctor/<int:doctor_id>/booking/", create_doctor_booking, name="create_doctor_booking"),
    path("lab/<int:lab_id>/booking/", create_lab_booking, name="create_lab_booking"),
    path("doctor/<int:pk>/review/", doctor_review),
    path("plans/", get_patient_plans),
    path("plans/<int:pk>/", get_patient_plan),
    path("take_medicine/<int:pk>/", take_medicine),
    
    
]