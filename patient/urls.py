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
    list_doctor_question,
    question_answer,
    list_lab_result,
    list_prescriptions,
    get_doctor_booking, 
)

urlpatterns = [
    # Create a booking with a doctor
    path("doctor/<int:doctor_id>/booking/",create_doctor_booking,name="create_doctor_booking",),
    # Create a booking with a lab
    path("lab/<int:lab_id>/booking/",create_lab_booking,name="create_lab_booking",),
    # Post a review for a doctor
    path(
        "doctor/<int:pk>/review/",
        doctor_review,
        name="doctor_review",
    ),
    
    # Get all patient plans
    path(
        "plans/",
        get_patient_plans,
        name="get_patient_plans",
    ),
    
    # Get a specific patient plan by doctor ID
    path(
        "plans/<int:pk>/",
        get_patient_plan,
        name="get_patient_plan",
    ),
    
    # Take a medicine or get details about a medicine by ID
    path(
        "take_medicine/<int:pk>/",
        take_medicine,
        name="take_medicine",
    ),
    
    # Get all doctor bookings for the logged-in patient
    path(
        "doctor_bookings/",
        get_doctor_bookings,
        name="get_doctor_bookings",
    ),
    
    # Get details of a specific doctor booking by ID
    path(
        "doctor_booking/<int:pk>/",
        get_doctor_booking,
        name="get_doctor_booking",
    ),
    
    # Get all lab bookings for the logged-in patient
    path(
        "lab_bookings/",
        get_lab_bookings,
        name="get_lab_bookings",
    ),
    
    # Cancel a specific doctor booking by ID
    path(
        "bookings/<int:pk>/cancel/",
        cancel_booking,
        name="cancel_booking",
    ),
    
    # List all tests associated with completed doctor bookings
    path(
        "doctor_tests/",
        list_doctor_tests,
        name="list_doctor_tests",
    ),
    
    # List a specific doctor's questions by test ID
    path(
        "doctor_questions/<int:pk>/",
        list_doctor_question,
        name="list_doctor_question",
    ),
    
    # Answer a specific question by question ID
    path(
        "question_answer/<int:pk>/",
        question_answer,
        name="question_answer",
    ),
    
    # List all lab results for the logged-in patient
    path(
        "lab_result/",
        list_lab_result,
        name="list_lab_result",
    ),
    
    # List all prescriptions for the logged-in patient
    path(
        "prescriptions/",
        list_prescriptions,
        name="list_prescriptions",
    ),
]
