# rest imports
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
# django imports
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
# swagger imports
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# internal imports
from .models import DoctorBooking, DoctorComment, PatientPlan, Prescription
from accounts.serializers import DoctorProfileSerializer
from .filters import DoctorFilter, DoctorBookingFilter
from patient.models import PatientMedicine, Test
from accounts.models import DoctorProfile, User
from .serializers import (
    DoctorListSerializer,
    DoctorPatientSerializer,
    PatientPlanDetailSerializer,
    PatientPlanSerializer,
    DoctorReadBookingDetailsSerializer,
    DoctorReadBookingSerializer,
    DoctorBookingReschdualAndCompleteSerializer,
    PatientMedicineCreateSerializer,
    PatientMedicineSerializer,
    PatientPlanSerializer,
    CreatePatientPlanSerializer,
    DoctorReviewsSerializer,
    DoctorCommentSerializer,
    QuestionSerializer,
    TestSerializer,
    PrescriptionSerializer,
    SimpleDocPrescriptionSerializer
)



@swagger_auto_schema(
    method='get',
    responses={200: DoctorListSerializer(many=True)}
)
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_all_docs(request):
    """
    Retrieve all doctors with pagination and filters.
    """
    filterset = DoctorFilter(
        request.GET,
        queryset=DoctorProfile.objects.select_related("user").order_by("rating"),
    )
    paginator = PageNumberPagination()
    paginator.page_size = 5
    queryset = paginator.paginate_queryset(filterset.qs, request)
    serializer = DoctorListSerializer(queryset, many=True, context={"request": request})
    return paginator.get_paginated_response(serializer.data)

@swagger_auto_schema(
    method='get',
    responses={
        200: DoctorProfileSerializer(),
        404: 'Doctor not found',
        400: 'User is not a doctor'
    }
)
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def doctor_detail(request, pk):
    """
    Retrieve detailed information about a specific doctor.
    """
    try:
        doctor = User.objects.get(id=pk)
    except User.DoesNotExist:
        return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)

    if doctor.role == "DOCTOR":
        try:
            doctor_profile = DoctorProfile.objects.get(user=doctor)
        except DoctorProfile.DoesNotExist:
            return Response({"error": "Doctor profile not found"}, status=status.HTTP_404_NOT_FOUND)

        doctor_bookings = DoctorBooking.objects.filter(doctor=doctor).count()
        doctor_profile.doctor_patients = doctor_bookings
        doctor_profile.save()

        serializer = DoctorProfileSerializer(doctor_profile, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"error": "User is not a doctor"}, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='get',
    responses={200: DoctorPatientSerializer(many=True)}
)
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def doctor_patients(request):
    """
    Retrieve all patients for the authenticated doctor.
    """
    doctor = request.user

    if doctor.role == "DOCTOR":
        bookings = DoctorBooking.objects.filter(doctor=doctor)
        patients = set(booking.patient for booking in bookings)
        paginator = PageNumberPagination()
        paginator.page_size = 5
        query_set = paginator.paginate_queryset(list(patients), request)
        serializer = DoctorPatientSerializer(query_set, many=True, context={"doctor": doctor, "request":request})
        return paginator.get_paginated_response(serializer.data)
    else:
        return Response({"detail": "User is not a doctor"}, status=403)

@swagger_auto_schema(
    method='get',
    responses={200: DoctorReadBookingSerializer(many=True)}
)
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_all_bookings(request):
    """
    Retrieve all bookings for the authenticated doctor with optional filtering.
    """
    queryset = DoctorBooking.objects.filter(doctor=request.user)
    filterset_class = DoctorBookingFilter
    filtered_queryset = filterset_class(request.query_params, queryset=queryset).qs
    paginator = PageNumberPagination()
    paginator.page_size = 5
    query_set = paginator.paginate_queryset(filtered_queryset, request)
    serializer = DoctorReadBookingSerializer(query_set, many=True, context={"request":request})
    return paginator.get_paginated_response(serializer.data)

@swagger_auto_schema(
    method='get',
    responses={
        200: DoctorReadBookingSerializer(),
        403: 'You do not have permission to view this booking.',
        404: 'Booking does not exist.'
    }
)
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def booking_detail(request, pk):
    """
    Retrieve detailed information about a specific booking.
    """
    user = request.user
    try:
        booking = DoctorBooking.objects.get(id=pk)
        if booking.doctor == user or booking.patient == user:
            serializer = DoctorReadBookingDetailsSerializer(booking, context={"request":request})
            return Response(serializer.data)
        else:
            return Response({"errors": "You do not have permission to view this booking."}, status=status.HTTP_403_FORBIDDEN)
    except DoctorBooking.DoesNotExist:
        return Response({"errors": "Booking does not exist."}, status=status.HTTP_404_NOT_FOUND)

@swagger_auto_schema(
    method='put',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'booking_date': openapi.Schema(type=openapi.TYPE_STRING, description='New booking date')
        }
    ),
    responses={
        200: DoctorBookingReschdualAndCompleteSerializer(),
        403: 'You do not have permission to reschedule this booking.',
        404: 'Booking does not exist.'
    }
)
@api_view(["PUT"])
@permission_classes([permissions.IsAuthenticated])
def reschedule_booking(request, pk):
    """
    Reschedule a specific booking.
    """
    user = request.user
    data = request.data
    new_booking_date = data["booking_date"]
    try:
        booking = DoctorBooking.objects.get(id=pk)
        if booking.doctor == user or booking.patient == user:
            booking.booking_date = new_booking_date
            booking.save()
            serializer = DoctorBookingReschdualAndCompleteSerializer(booking)
            return Response(serializer.data)
        else:
            return Response({"errors": "You do not have permission to reschedule this booking."}, status=status.HTTP_403_FORBIDDEN)
    except DoctorBooking.DoesNotExist:
        return Response({"errors": "Booking does not exist."}, status=status.HTTP_404_NOT_FOUND)

@swagger_auto_schema(
    method='put',
    responses={
        200: DoctorBookingReschdualAndCompleteSerializer(),
        403: 'You do not have permission to complete this booking.',
        404: 'Booking does not exist.',
        400: 'This booking is already completed or canceled.'
    }
)
@api_view(["PUT"])
@permission_classes([permissions.IsAuthenticated])
def complete_booking(request, pk):
    """
    Mark a specific booking as completed.
    """
    user = request.user
    try:
        booking = DoctorBooking.objects.get(id=pk)
        if booking.doctor == user:
            if booking.status == "completed":
                return Response("This booking is already completed", status=status.HTTP_400_BAD_REQUEST)
            if booking.status == "canceled":
                return Response("This booking is already canceled", status=status.HTTP_400_BAD_REQUEST)
            booking.status = "completed"
            booking.save()
            serializer = DoctorBookingReschdualAndCompleteSerializer(booking)
            return Response(serializer.data)
        else:
            return Response({"errors": "You do not have permission to complete this booking."}, status=status.HTTP_403_FORBIDDEN)
    except DoctorBooking.DoesNotExist:
        return Response({"errors": "Booking does not exist."}, status=status.HTTP_404_NOT_FOUND)

@swagger_auto_schema(
    method='get',
    responses={
        200: PatientPlanDetailSerializer(),
        401: 'You have to be a doctor to use this function',
        404: 'Patient or Patient Plan not found'
    }
)
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_patient_plan(request, pk):
    """
    Retrieve the patient plan for a specific patient.
    """
    doctor = request.user
    if doctor.role != "DOCTOR":
        return Response({"message:": "You have to be a doctor to use this function"}, status=status.HTTP_401_UNAUTHORIZED)
    patient_plan = get_object_or_404(PatientPlan, id=pk)
    if patient_plan.doctor != doctor:
        return Response({"message:": "You don't have access for this plan"}, status=status.HTTP_401_UNAUTHORIZED)        
    serializer = PatientPlanDetailSerializer(patient_plan, context={"request":request})
    return Response(serializer.data)

@swagger_auto_schema(
    method='get',
    responses={
        200: PatientPlanSerializer(),
        401: 'You have to be a doctor to use this function',
        404: 'Patient or Patient Plan not found'
    }
)
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_patient_plans(request):
    """
    Retrieve the patient plan for a specific patient.
    """
    doctor = request.user
    if doctor.role != "DOCTOR":
        return Response({"message:": "You have to be a doctor to use this function"}, status=status.HTTP_401_UNAUTHORIZED)
    patient_plans = PatientPlan.objects.filter(doctor=doctor)        
    serializer = PatientPlanSerializer(patient_plans, context={"request":request}, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='post',
    responses={
        201: CreatePatientPlanSerializer(),
        401: 'You have to be a doctor to use this function',
        400: 'Invalid data provided'
    }
)
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_patient_plan(request, pk):
    """
    Create a patient plan for a specific patient.
    """
    doctor = request.user
    patient = get_object_or_404(User, id=pk)
    if doctor.role != "DOCTOR":
        return Response({"message:": "You have to be a doctor to use this function"}, status=status.HTTP_401_UNAUTHORIZED)
    if patient.role != "PATIENT":
        return Response({"message:": "You have to be a patient to use this function"}, status=status.HTTP_401_UNAUTHORIZED)
    data = {"doctor": doctor.id, "patient": patient.id}
    serializer = CreatePatientPlanSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='post',
    request_body=PatientMedicineCreateSerializer,
    responses={
        201: PatientMedicineCreateSerializer(),
        400: 'Invalid data provided'
    }
)
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_patient_medicine(request):
    """
    Create a medicine entry for a patient.
    """
    serializer = PatientMedicineCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='get',
    responses={
        200: PatientMedicineSerializer(),
        404: 'Patient Medicine not found'
    }
)
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_patient_medicine(request, pk):
    """
    Retrieve the details of a specific patient medicine.
    """
    patient_medicine = get_object_or_404(PatientMedicine, pk=pk)
    serializer = PatientMedicineSerializer(patient_medicine)
    return Response(serializer.data)

@swagger_auto_schema(
    method='get',
    responses={
        200: DoctorReviewsSerializer(many=True),
        401: 'You have to be a doctor to use this function'
    }
)
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_doctor_reviews(request):
    """
    Retrieve reviews for the authenticated doctor.
    """
    doctor = request.user
    if doctor.role != "DOCTOR":
        return Response("You have to be a doctor to use this function!", status=status.HTTP_401_UNAUTHORIZED)
    doctor_bookings = DoctorBooking.objects.filter(doctor=doctor, status="completed")
    serializer = DoctorReviewsSerializer(doctor_bookings, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='post',
    request_body=DoctorCommentSerializer,
    responses={
        201: DoctorCommentSerializer(),
        401: 'You don\'t have permission',
        404: 'Patient or Booking not found',
        400: 'Invalid data provided'
    }
)
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def doctor_comment(request, pk):
    """
    Add a comment for a specific booking or patient.
    """
    data = request.data
    doctor = request.user
    if doctor.role != "DOCTOR":
        return Response({"message:": "You don't have permission"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        booking = DoctorBooking.objects.get(id=pk)
    except DoctorBooking.DoesNotExist:
        try:
            patient = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)
        booking = DoctorBooking.objects.filter(doctor=doctor, patient=patient, status="completed").last()
        if not booking:
            return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = DoctorCommentSerializer(data=data)
    if serializer.is_valid():
        serializer.save(booking=booking)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='get',
    responses={
        200: DoctorCommentSerializer(many=True),
        404: 'Patient not found'
    }
)
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def list_doctor_comments(request, pk):
    """
    List comments made by the doctor for a specific patient.
    """
    doctor = request.user
    try:
        patient = User.objects.get(id=pk)
    except User.DoesNotExist:
        return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)

    comments = DoctorComment.objects.filter(booking__doctor=doctor, booking__patient=patient)
    serializer = DoctorCommentSerializer(comments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='post',
    request_body=QuestionSerializer,
    responses={
        201: QuestionSerializer(),
        404: 'Test not found',
        400: 'Invalid data provided'
    }
)
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def add_question(request, pk):
    """
    Add a question to a specific test.
    """
    try:
        test = Test.objects.get(id=pk)
    except Test.DoesNotExist:
        return Response({"error": "Test not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = QuestionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(test=test)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='post',
    responses={
        201: TestSerializer(),
        401: 'You don\'t have permission',
        404: 'Booking not found'
    }
)
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_test(request, pk):
    """
    Create a test for a specific booking.
    """
    doctor = request.user
    if doctor.role != "DOCTOR":
        return Response({"message:": "You don't have permission"}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        booking = DoctorBooking.objects.get(id=pk)
    except DoctorBooking.DoesNotExist:
        return Response({"message:": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)
    test = Test.objects.create(booking=booking)
    serializer = TestSerializer(test, context={"request":request})
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@swagger_auto_schema(
    method='get',
    responses={
        200: TestSerializer(many=True),
        401: 'You don\'t have permission',
        404: 'Patient not found'
    }
)
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def list_patient_tests(request, pk):
    """
    List all tests for a specific patient.
    """
    doctor = request.user
    try:
        patient = User.objects.get(id=pk)
    except User.DoesNotExist:
        return Response({"message": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)

    if doctor.role != "DOCTOR" or patient.role != "PATIENT":
        return Response({"message": "You don't have permission"}, status=status.HTTP_403_FORBIDDEN)

    bookings = DoctorBooking.objects.filter(patient=patient, doctor=doctor, status="completed")
    tests = Test.objects.filter(booking__in=bookings)
    paginator = PageNumberPagination()
    paginator.page_size = 5
    query_set = paginator.paginate_queryset(list(tests), request)
    serializer = TestSerializer(query_set, many=True, context={"request":request})
    return paginator.get_paginated_response(serializer.data)

@swagger_auto_schema(
    method='get',
    responses={
        200: TestSerializer(),
        403: 'You don\'t have permission',
        404: 'Test not found'
    }
)
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def list_patient_question(request, pk):
    """
    List all questions for a specific test.
    """
    doctor = request.user
    if doctor.role != "DOCTOR":
        return Response({"message": "You don't have permission"}, status=status.HTTP_403_FORBIDDEN)
    try:
        test = Test.objects.get(id=pk)
    except Test.DoesNotExist:
        return Response({"message": "Test not found"}, status=status.HTTP_404_NOT_FOUND)
    if test.booking.doctor != doctor:
        return Response({"message": "You don't have permission"}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = TestSerializer(test, context={"request":request})
    return Response(serializer.data)

@swagger_auto_schema(
    method='post',
    responses={
        201: PrescriptionSerializer(),
        401: 'You have to be a doctor to use this function',
        404: 'Patient Plan not found',
        400: 'Invalid data provided'
    }
)
@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_prescription(request, pk):
    """
    Create a prescription for a specific patient plan.
    """
    doctor = request.user
    if doctor.role != "DOCTOR":
        return Response("You have to be a doctor to use this function", status=status.HTTP_401_UNAUTHORIZED)
    try:
        patient_plan = PatientPlan.objects.get(id=pk)
        prescription = Prescription.objects.create(patient_plan=patient_plan)
        serializer = PrescriptionSerializer(prescription)
    except Exception as e:
        return Response({"errors:": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@swagger_auto_schema(
    method='get',
    responses={
        200: SimpleDocPrescriptionSerializer(many=True),
        401: 'You have to be a doctor to use this function',
        404: 'Patient not found'
    }
)
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def list_prescriptions(request, pk):
    """
    List all prescriptions for a specific patient.
    """
    doctor = request.user
    if doctor.role != "DOCTOR":
        return Response("You have to be a doctor to use this function", status=status.HTTP_401_UNAUTHORIZED)
    try:
        patient = User.objects.get(id=pk)
        patient_plans = PatientPlan.objects.filter(doctor=doctor, patient=patient)
        prescriptions = Prescription.objects.filter(patient_plan__in=patient_plans)
        paginator = PageNumberPagination()
        paginator.page_size = 5
        query_set = paginator.paginate_queryset(list(prescriptions), request)
        serializer = SimpleDocPrescriptionSerializer(query_set, many=True, context={"request":request})
    except Exception as e:
        return Response({"errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return paginator.get_paginated_response(serializer.data)

@swagger_auto_schema(
    method='get',
    responses={
        200: PrescriptionSerializer(),
        404: 'Prescription not found'
    }
)
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def prescription_details(request, pk):
    """
    Retrieve the details of a specific prescription.
    """
    try:
        prescription = Prescription.objects.get(id=pk)
        serializer = PrescriptionSerializer(prescription)
    except Exception as e:
        return Response({"errors": str(e)}, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.data)