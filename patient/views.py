# internal imports
from chat.models import Connection
from doctor.models import DoctorBooking, PatientPlan, Prescription
from patient.models import PatientMedicine, Question, Test
from laboratory.models import LabBooking, Laboratory
from laboratory.filters import LabBookingFilter
from doctor.filters import DoctorBookingFilter
from orders.models import CreditCard
from accounts.models import User
from doctor.serializers import (
    DoctorBookingCancelSerializer,
    DoctorReadBookingSerializer,
    PatientMedicineSerializer,
    QuestionSerializer,
    TestSerializer,
    SimplePatientPrescriptionSerializer
)
from laboratory.serializers import LabReadBookingSerializer, LabResultSerializer
from patient.serializers import ( 
    PatientReadBookingDetailsSerializer,
    DoctorPatientPlanDetailSerializer,
    PatientReadBookingSerializer,
    DoctorBookingSerializer,
    LabBookingSerializer,
    DoctorPlanSerializer,
)
# rest imports
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
# django imports
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Avg
# swagger imports
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



# Schema definitions for Swagger documentation
doctor_id_param = openapi.Parameter('doctor_id', openapi.IN_PATH, description="ID of the doctor", type=openapi.TYPE_INTEGER)
lab_id_param = openapi.Parameter('lab_id', openapi.IN_PATH, description="ID of the lab", type=openapi.TYPE_INTEGER)
booking_id_param = openapi.Parameter('pk', openapi.IN_PATH, description="ID of the booking", type=openapi.TYPE_INTEGER)
question_id_param = openapi.Parameter('pk', openapi.IN_PATH, description="ID of the question", type=openapi.TYPE_INTEGER)
payment_card_schema = openapi.Schema(type=openapi.TYPE_STRING, description="Payment card ID")

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'payment_card': payment_card_schema}
    ),
    responses={201: DoctorBookingSerializer, 400: 'Bad Request'}
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_doctor_booking(request, doctor_id):
    """
    Create a booking with a doctor.
    """
    try:
        doctor = User.objects.get(id=doctor_id)
    except User.DoesNotExist:
        return Response(
            {"error": "Invalid Doctor ID", "message": "Please provide a valid Doctor ID."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if doctor.role != "DOCTOR":
        return Response(
            {"error": "Invalid Doctor ID", "message": "Please provide a valid Doctor ID."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    data = request.data
    user = request.user

    try:
        payment_card = data["payment_card"]
        card = CreditCard.objects.get(id=payment_card)
        if card.user != user:
            return Response(
                {"errors": "You are not the owner of this card"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    except KeyError:
        return Response(
            {"errors": "Payment card ID is missing"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except CreditCard.DoesNotExist:
        return Response(
            {"errors": "Payment card not found"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    bookings = DoctorBooking.objects.filter(patient=user, doctor=doctor).count()
    if bookings == 0:
            connection = Connection.objects.create(sender=user, receiver=doctor)


    serializer = DoctorBookingSerializer(
        data=data,
        context={"patient_id": user.id, "doctor_id": doctor_id, "payment_card": payment_card, "connection_id":connection.id},
    )


    if serializer.is_valid():
        serializer.save()
    
    
        return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)
    else:
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'payment_card': payment_card_schema}
    ),
    responses={201: LabBookingSerializer, 400: 'Bad Request'}
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_lab_booking(request, lab_id):
    """
    Create a booking with a lab.
    """
    try:
        lab = Laboratory.objects.get(id=lab_id)
    except Laboratory.DoesNotExist:
        return Response(
            {"error": "Invalid Lab ID", "message": "Please provide a valid Lab ID."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    data = request.data
    user = request.user

    try:
        payment_card = data["payment_card"]
        card = CreditCard.objects.get(id=payment_card)
        if card.user != user:
            return Response(
                {"errors": "You are not the owner of this card"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    except KeyError:
        return Response(
            {"errors": "Payment card ID is missing"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except CreditCard.DoesNotExist:
        return Response(
            {"errors": "Payment card not found"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer = LabBookingSerializer(
        data=data,
        context={"patient_id": user.id, "lab_id": lab_id, "payment_card": payment_card},
    )

    if serializer.is_valid():
        serializer.save()
        return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)
    else:
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'rating': openapi.Schema(type=openapi.TYPE_INTEGER, description="Rating"),
            'review': openapi.Schema(type=openapi.TYPE_STRING, description="Review")
        }
    ),
    responses={200: DoctorReadBookingSerializer, 400: 'Bad Request'}
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def doctor_review(request, pk):
    """
    Post a review for a doctor.
    """
    if request.user.role != "PATIENT":
        return Response(
            {"message": "You have to be a patient to make a review"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    patient = request.user
    data = request.data

    try:
        doctor = User.objects.get(id=pk)
    except User.DoesNotExist:
        return Response(
            {"message": "Enter a valid doctor ID"}, status=status.HTTP_404_NOT_FOUND
        )

    if doctor.role != "DOCTOR":
        return Response(
            {"message": "Enter a valid doctor ID"}, status=status.HTTP_400_BAD_REQUEST
        )

    booking = DoctorBooking.objects.filter(
        patient=patient, doctor=doctor, status="completed"
    ).last()

    if not booking:
        return Response(
            {"message": "You don't have a booking with this doctor or you have not completed your booking"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    rating = data.get("rating")
    if rating is not None:
        booking.rating = rating

        # Calculate average rating and update DoctorProfile
        doctor_profile = doctor.doctor_profile
        average_rating = DoctorBooking.objects.filter(
            doctor=doctor, rating__isnull=False
        ).aggregate(Avg("rating"))["rating__avg"]
        doctor_profile.rating = average_rating
        doctor_profile.save()

    booking.review = data.get("review", "")
    booking.save()

    serializer = DoctorReadBookingSerializer(booking, context={"request":request})
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    responses={200: DoctorPlanSerializer(many=True)}
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_patient_plans(request):
    """
    Get all patient plans for the logged-in patient.
    """
    patient = request.user
    if patient.role != "PATIENT":
        return Response(
            {"message:": "you have to be a patient to use this function"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    patient_plans = PatientPlan.objects.filter(patient=patient)
    serializer = DoctorPlanSerializer(patient_plans, many=True, context={"request": request})
    return Response(serializer.data)


@swagger_auto_schema(
    method='get',
    responses={200: DoctorPatientPlanDetailSerializer, 401: 'Unauthorized', 404: 'Not Found'}
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_patient_plan(request, pk):
    """
    Get a specific patient plan by doctor ID.
    """
    patient = request.user
    if patient.role != "PATIENT":
        return Response(
            {"message:": "You have to be a patient to use this function"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    try:
        patient_plan = PatientPlan.objects.get(id=pk)
    except PatientPlan.DoesNotExist:
        return Response({"message:": "Patient plan does not exist"}, status=status.HTTP_404_NOT_FOUND)
    serializer = DoctorPatientPlanDetailSerializer(patient_plan, context={"request": request})
    return Response(serializer.data)


@swagger_auto_schema(
    method='post',
    responses={200: PatientMedicineSerializer, 401: 'Unauthorized', 404: 'Not Found'}
)
@swagger_auto_schema(
    method='get',
    responses={200: PatientMedicineSerializer, 401: 'Unauthorized', 404: 'Not Found'}
)
@api_view(["POST", "GET"])
@permission_classes([IsAuthenticated])
def take_medicine(request, pk):
    """
    Take a medicine or get details about a medicine by ID.
    """
    patient = request.user
    medicine = get_object_or_404(PatientMedicine, id=pk)
    if request.method == "POST":
        if patient.role != "PATIENT":
            return Response(
                {"message": "You have to be a patient to use this function"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        medicine.left -= 1
        medicine.save()
        serializer = PatientMedicineSerializer(medicine)
        return Response(serializer.data)

    if request.method == "GET":
        get_serializer = PatientMedicineSerializer(medicine)
        return Response(get_serializer.data)


@swagger_auto_schema(
    method='get',
    responses={200: PatientReadBookingSerializer(many=True)}
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_doctor_bookings(request):
    """
    Get all doctor bookings for the logged-in patient.
    """
    queryset = DoctorBooking.objects.filter(patient=request.user)

    # Applying filter if 'status' parameter is provided in the request
    filter_backends = [DjangoFilterBackend]
    filterset_class = DoctorBookingFilter

    filtered_queryset = filterset_class(request.query_params, queryset=queryset).qs

    serializer = PatientReadBookingSerializer(filtered_queryset, many=True, context={"request": request})
    return Response(serializer.data)


@swagger_auto_schema(
    method='get',
    responses={200: PatientReadBookingDetailsSerializer, 401: 'Unauthorized', 404: 'Not Found'}
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_doctor_booking(request, pk):
    """
    Get details of a specific doctor booking by ID.
    """
    try:
        booking = DoctorBooking.objects.get(id=pk)
        patient = request.user
        if patient.role != 'PATIENT' or booking.patient != patient:
            return Response({"errors": "You don't have access to this function"}, status=status.HTTP_403_FORBIDDEN)
    except DoctorBooking.DoesNotExist:
        return Response({"errors": "Booking does not exist"}, status=status.HTTP_404_NOT_FOUND)

    serializer = PatientReadBookingDetailsSerializer(booking, context={"request": request})
    return Response(serializer.data)


@swagger_auto_schema(
    method='get',
    responses={200: LabReadBookingSerializer(many=True)}
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_lab_bookings(request):
    """
    Get all lab bookings for the logged-in patient.
    """
    queryset = LabBooking.objects.filter(patient=request.user)

    # Applying the filter
    filter_backends = [DjangoFilterBackend]
    filterset_class = LabBookingFilter

    filtered_queryset = filterset_class(request.query_params, queryset=queryset).qs

    serializer = LabReadBookingSerializer(filtered_queryset, many=True, context={"request": request})
    return Response(serializer.data)


@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'cancel_reason': openapi.Schema(type=openapi.TYPE_STRING, description="Reason for cancellation")}
    ),
    responses={200: DoctorBookingCancelSerializer, 403: 'Forbidden', 404: 'Not Found'}
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def cancel_booking(request, pk):
    """
    Cancel a specific doctor booking by ID.
    """
    user = request.user
    data = request.data
    try:
        booking = DoctorBooking.objects.get(id=pk)
        if booking.patient == user:
            if booking.status == "completed":
                return Response(
                    "This booking is already completed",
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if booking.status == "canceled":
                return Response(
                    "This booking is already canceled",
                    status=status.HTTP_400_BAD_REQUEST,
                )
            booking.cancel_reason = data.get("cancel_reason", "")
            booking.status = "canceled"  # Update the status field
            booking.save()
            serializer = DoctorBookingCancelSerializer(booking)
            return Response(serializer.data)
        else:
            return Response(
                {"errors": "You do not have permission to cancel this booking."},
                status=status.HTTP_403_FORBIDDEN,
            )
    except DoctorBooking.DoesNotExist:
        return Response(
            {"errors": "Booking does not exist."}, status=status.HTTP_404_NOT_FOUND
        )


@swagger_auto_schema(
    method='get',
    responses={200: TestSerializer(many=True)}
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_doctor_tests(request):
    """
    List all tests associated with completed doctor bookings.
    """
    patient = request.user
    bookings = DoctorBooking.objects.filter(patient=patient, status="completed")
    tests = Test.objects.filter(booking__in=bookings)
    paginator = PageNumberPagination()
    paginator.page_size = 5
    query_set = paginator.paginate_queryset(list(tests), request)
    serializer = TestSerializer(query_set, many=True, context={"request": request})
    return paginator.get_paginated_response(serializer.data)


@swagger_auto_schema(
    method='get',
    responses={200: TestSerializer, 403: 'Forbidden', 404: 'Not Found'}
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_doctor_question(request, pk):
    """
    List a specific doctor's questions by test ID.
    """
    patient = request.user
    if patient.role != "PATIENT":
        return Response({"message": "You don't have permission"}, status=status.HTTP_403_FORBIDDEN)
    test = get_object_or_404(Test, id=pk)
    if test.booking.patient != patient:
        return Response({"message": "You don't have permission"}, status=status.HTTP_403_FORBIDDEN)
    serializer = TestSerializer(test, context={"request":request})
    return Response(serializer.data)


@swagger_auto_schema(
    method='put',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={'answer': openapi.Schema(type=openapi.TYPE_STRING, description="Answer to the question")}
    ),
    responses={200: QuestionSerializer, 403: 'Forbidden', 404: 'Not Found'}
)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def question_answer(request, pk):
    """
    Answer a specific question by question ID.
    """
    patient = request.user
    data = request.data
    if patient.role != "PATIENT":
        return Response({"message": "You don't have permission"}, status=status.HTTP_403_FORBIDDEN)
    question = get_object_or_404(Question, id=pk)
    if question.test.booking.patient != patient:
        return Response({"message": "You don't have permission"}, status=status.HTTP_403_FORBIDDEN)
    question.answer = data["answer"]
    question.save()
    serializer = QuestionSerializer(question)
    return Response(serializer.data)


@swagger_auto_schema(
    method='get',
    responses={200: LabResultSerializer(many=True)}
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_lab_result(request):
    """
    List all lab results for the logged-in patient.
    """
    patient = request.user
    lab_bookings = LabBooking.objects.filter(patient=patient)
    paginator = PageNumberPagination()
    paginator.page_size = 5
    query_set = paginator.paginate_queryset(list(lab_bookings), request)
    serializer = LabResultSerializer(query_set, context={"request": request}, many=True)
    return paginator.get_paginated_response(serializer.data)


@swagger_auto_schema(
    method='get',
    responses={200: SimplePatientPrescriptionSerializer(many=True)}
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_prescriptions(request):
    """
    List all prescriptions for the logged-in patient.
    """
    patient = request.user
    if patient.role != "PATIENT":
        return Response("You have to be a patient to use this function", status=status.HTTP_401_UNAUTHORIZED)
    try:
        patient_plans = PatientPlan.objects.filter(patient=patient)
        prescriptions = Prescription.objects.filter(patient_plan__in=patient_plans)
        paginator = PageNumberPagination()
        paginator.page_size = 5
        query_set = paginator.paginate_queryset(list(prescriptions), request)
        serializer = SimplePatientPrescriptionSerializer(query_set, many=True, context={"request": request})
    except Exception as e:
        return Response({"errors": e})
    return paginator.get_paginated_response(serializer.data)