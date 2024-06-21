from accounts.models import DoctorProfile, User
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status


from patient.models import PatientMedicine, Test
from .filters import DoctorFilter, DoctorBookingFilter
from rest_framework.pagination import PageNumberPagination
from .serializers import (
    DoctorListSerializer,
    DoctorPatientSerializer,
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
)
from rest_framework.response import Response
from accounts.serializers import DoctorProfileSerializer
from .models import DoctorBooking, DoctorComment, PatientPlan, Prescription
from rest_framework import filters

# from .filters import DoctorBookingFilter
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_all_docs(request):
    filterset = DoctorFilter(
        request.GET,
        queryset=DoctorProfile.objects.select_related("user").order_by("rating"),
    )
    paginator = PageNumberPagination()
    paginator.page_size = 5
    queryset = paginator.paginate_queryset(filterset.qs, request)

    serializer = DoctorListSerializer(queryset, many=True, context={"request": request})

    return paginator.get_paginated_response(serializer.data)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def doctor_detail(request, pk):
    try:
        doctor = User.objects.get(id=pk)
    except User.DoesNotExist:
        return Response({"error": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)

    if doctor.role == "DOCTOR":
        try:
            doctor_profile = DoctorProfile.objects.get(user=doctor)
        except DoctorProfile.DoesNotExist:
            return Response(
                {"error": "Doctor profile not found"}, status=status.HTTP_404_NOT_FOUND
            )

        doctor_bookings = DoctorBooking.objects.filter(doctor=doctor).count()
        doctor_profile.doctor_patients = doctor_bookings
        doctor_profile.save()

        serializer = DoctorProfileSerializer(
            doctor_profile, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(
            {"error": "User is not a doctor"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def doctor_patients(request):
    doctor = request.user

    if doctor.role == "DOCTOR":
        bookings = DoctorBooking.objects.filter(doctor=doctor, status="completed")
        patients = set(booking.patient for booking in bookings)

        # Serialize the patients with context
        serializer = DoctorPatientSerializer(
            patients, many=True, context={"doctor": doctor}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "User is not a doctor"}, status=403)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_all_bookings(request):
    queryset = DoctorBooking.objects.filter(doctor=request.user)

    # Applying filter if 'status' parameter is provided in the request
    filter_backends = [DjangoFilterBackend]
    filterset_class = DoctorBookingFilter

    filtered_queryset = filterset_class(request.query_params, queryset=queryset).qs

    serializer = DoctorReadBookingSerializer(filtered_queryset, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def booking_detail(request, pk):
    user = request.user
    try:
        booking = DoctorBooking.objects.get(id=pk)
        if booking.doctor == user or booking.patient == user:
            serializer = DoctorReadBookingSerializer(booking)
            return Response(serializer.data)
        else:
            return Response(
                {"errors": "You do not have permission to view this booking."},
                status=status.HTTP_403_FORBIDDEN,
            )
    except DoctorBooking.DoesNotExist:
        return Response(
            {"errors": "Booking does not exist."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["PUT"])
@permission_classes([permissions.IsAuthenticated])
def reschedual_booking(request, pk):
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
            return Response(
                {"errors": "You do not have permission to reschedual this booking."},
                status=status.HTTP_403_FORBIDDEN,
            )
    except DoctorBooking.DoesNotExist:
        return Response(
            {"errors": "Booking does not exist."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["PUT"])
@permission_classes([permissions.IsAuthenticated])
def complete_booking(request, pk):
    user = request.user
    data = request.data
    try:
        booking = DoctorBooking.objects.get(id=pk)
        if booking.doctor == user:
            if booking.status == "completed":
                return Response(
                    "this booking is already completed",
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if booking.status == "canceled":
                return Response(
                    "this booking is already canceled",
                    status=status.HTTP_400_BAD_REQUEST,
                )
            booking.status = "completed"
            booking.save()
            serializer = DoctorBookingReschdualAndCompleteSerializer(booking)
            return Response(serializer.data)
        else:
            return Response(
                {"errors": "You do not have permission to complete this booking."},
                status=status.HTTP_403_FORBIDDEN,
            )
    except DoctorBooking.DoesNotExist:
        return Response(
            {"errors": "Booking does not exist."}, status=status.HTTP_404_NOT_FOUND
        )


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_patient_plan(request, pk):
    doctor = request.user
    patient = get_object_or_404(User, id=pk)
    if doctor.role != "DOCTOR":
        return Response(
            {"message:": "you have to be a doctor to use this function"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    if patient.role != "PATIENT":
        return Response(
            {"message:": "you have to be a user to use this function"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    patient_plan = get_object_or_404(PatientPlan, patient=patient, doctor=doctor)
    serializer = PatientPlanSerializer(patient_plan)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_patient_plan(request, pk):
    doctor = request.user
    patient = get_object_or_404(User, id=pk)
    if doctor.role != "DOCTOR":
        return Response(
            {"message:": "you have to be a doctor to use this function"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    if patient.role != "PATIENT":
        return Response(
            {"message:": "you have to be a user to use this function"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    data = {
        "doctor": doctor.id,
        "patient": patient.id,
    }

    serializer = CreatePatientPlanSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_patient_medicine(request):
    serializer = PatientMedicineCreateSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_patient_medicine(request, pk):
    patient_medicine = get_object_or_404(PatientMedicine, pk=pk)
    serializer = PatientMedicineSerializer(patient_medicine)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_doctor_reviews(request):
    doctor = request.user
    if doctor.role != "DOCTOR":
        return Response(
            "you have to be a doctor to use this function!",
            status=status.HTTP_401_UNAUTHORIZED,
        )
    doctor_bookings = DoctorBooking.objects.filter(doctor=doctor, status="completed")
    # print(doctor_bookings)
    serializer = DoctorReviewsSerializer(doctor_bookings, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def doctor_comment(request, pk):
    data = request.data
    doctor = request.user

    if doctor.role != "DOCTOR":
        return Response(
            {"message:": "you don't have permission"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    try:
        # Try to get the booking by ID
        booking = DoctorBooking.objects.get(id=pk)
    except DoctorBooking.DoesNotExist:
        # If booking not found by ID, try to get the patient by ID
        try:
            patient = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response(
                {"error": "patient not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # If patient found, get the last completed booking for that patient with the current doctor
        booking = DoctorBooking.objects.filter(
            doctor=doctor, patient=patient, status="completed"
        ).last()
        if not booking:
            return Response(
                {"error": "booking not found"}, status=status.HTTP_404_NOT_FOUND
            )

    serializer = DoctorCommentSerializer(data=data)
    if serializer.is_valid():
        serializer.save(booking=booking)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def list_doctor_comments(request, pk):
    doctor = request.user
    try:
        patient = User.objects.get(id=pk)
    except User.DoesNotExist:
        return Response(
            {"error": "patient not found"}, status=status.HTTP_404_NOT_FOUND
        )

    comments = DoctorComment.objects.filter(
        booking__doctor=doctor, booking__patient=patient
    )
    serializer = DoctorCommentSerializer(comments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def add_question(request, pk):
    try:
        test = Test.objects.get(id=pk)
    except Test.DoesNotExist:
        return Response({"error": "Test not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = QuestionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(test=test)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_test(request, pk):
    doctor = request.user
    if doctor.role != "DOCTOR":
        return Response(
            {"message:": "you don't have permission"},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    try:
        booking = DoctorBooking.objects.get(id=pk)
    except DoctorBooking.DoesNotExist:
        return Response(
            {"message:": "booking not found"}, status=status.HTTP_404_NOT_FOUND
        )
    test = Test.objects.create(booking=booking)
    serializer = TestSerializer(test)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def list_patient_tests(request, pk):
    doctor = request.user
    try:
        patient = User.objects.get(id=pk)
    except User.DoesNotExist:
        return Response({"message": "Patient not found"}, status=404)

    if doctor.role != "DOCTOR" or patient.role != "PATIENT":
        return Response({"message": "You don't have permission"}, status=403)

    bookings = DoctorBooking.objects.filter(
        patient=patient, doctor=doctor, status="completed"
    )
    tests = Test.objects.filter(booking__in=bookings)
    serializer = TestSerializer(tests, many=True)
    return Response(serializer.data, status=200)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def list_patient_question(request, pk):
    doctor = request.user
    if doctor.role != "DOCTOR":
        return Response({"message": "You don't have permission"}, status=403)
    test = Test.objects.get(id=pk)
    if test.booking.doctor != doctor:
        return Response({"message": "You don't have permission"}, status=403)
    serializer = TestSerializer(test)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_prescription(request, pk):
    doctor = request.user
    if doctor.role != "DOCTOR":
        return Response("you have to be a doctor to use this function", status=401)
    try:
        patient_plan = PatientPlan.objects.get(id=pk)
        prescription = Prescription.objects.create(patient_plan=patient_plan)
        serializer = PrescriptionSerializer(prescription)
    except Exception as e:
        return Response({"errors:": e})
    return Response(serializer.data, status=201)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def list_prescriptions(request, pk):
    doctor = request.user
    if doctor.role != "DOCTOR":
        return Response("you have to be a doctor to use this function", status=401)
    try:
        patient = User.objects.get(id=pk)
        patient_plans = PatientPlan.objects.filter(doctor=doctor, patient=patient)
        prescriptions = Prescription.objects.filter(patient_plan__in=patient_plans)
        serializer = PrescriptionSerializer(prescriptions, many=True)
    except Exception as e:
        return Response({"errors": e})
    return Response(serializer.data, status=200)
