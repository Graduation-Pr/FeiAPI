from django.urls import path
from .views import (
    get_all_docs,
    doctor_detail,
    get_all_bookings,
    booking_detail,
    reschedule_booking,
    complete_booking,
    doctor_patients,
    get_patient_plan,
    get_patient_plans,
    create_patient_plan,
    create_patient_medicine,
    get_patient_medicine,
    get_doctor_reviews,
    doctor_comment,
    list_doctor_comments,
    add_question,
    create_test,
    list_patient_tests,
    list_patient_question,
    create_prescription,
    list_prescriptions,
    prescription_details,
)

# Define URL patterns for the application
urlpatterns = [
    # Doctor-related paths
    path("", get_all_docs, name="doctor-list"),  
    path("<int:pk>/", doctor_detail, name="doctor-detail"),  
    path("reviews/", get_doctor_reviews, name="doctor-reviews"),  
    
    # Booking-related paths
    path("bookings/", get_all_bookings, name="booking-list"),  
    path("bookings/<int:pk>/", booking_detail, name="booking-detail"), 
    path("bookings/<int:pk>/reschedule/", reschedule_booking, name="reschedule-booking"),
    path("bookings/<int:pk>/complete/", complete_booking, name="complete-booking"), 

    # Patient-related paths
    path("patients/", doctor_patients, name="doctor-patients"),  
    
    # Patient plan-related paths
    path("patient_plans/", get_patient_plans, name="get-patient-plan"),  
    path("patient_plan/<int:pk>/", get_patient_plan, name="get-patient-plan"),  
    path("create/patient_plan/<int:pk>/", create_patient_plan, name="create-patient-plan"), 
    
    # Patient medicine-related paths
    path("create/patient_medicine/", create_patient_medicine, name="create-patient-medicine"),  
    path("patient_medicine/<int:pk>/", get_patient_medicine, name="get-patient-medicine"),  
    
    # Doctor comments-related paths
    path("comment/<int:pk>/", doctor_comment, name="doctor-comment"),  
    path("comments/<int:pk>/", list_doctor_comments, name="doctor-comments"),  
    
    # Test-related paths
    path("question/<int:pk>/", add_question, name="add-question"), 
    path("test/<int:pk>/", create_test, name="create-test"),  
    path("tests/<int:pk>/", list_patient_tests, name="list-patient-tests"), 
    path("tests/questions/<int:pk>/", list_patient_question, name="list-patient-questions"),  
    
    # Prescription-related paths
    path("prescription/<int:pk>/", create_prescription, name="create-prescription"),  
    path("prescriptions/<int:pk>/", list_prescriptions, name="list-prescriptions"),  
    path("prescription_details/<int:pk>/", prescription_details, name="prescription-details"),  
]
