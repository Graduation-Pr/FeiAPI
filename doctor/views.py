from django.shortcuts import render
from accounts.models import DoctorProfile, User
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from .filters import DoctorFilter
from rest_framework.pagination import PageNumberPagination
from .serializers import DoctorListSerializer, DoctorReadBookingSerializer
from rest_framework.response import Response
from rest_framework import generics
from accounts.serializers import DoctorProfileSerializer
from .models import DoctorBooking


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_all_docs(request):
    # Assuming DoctorProfileFilter is adjusted to work with DoctorProfile instances
    filterset = DoctorFilter(
        request.GET,
        queryset=DoctorProfile.objects.select_related("user").order_by("rating"),
    )
    paginator = PageNumberPagination()
    paginator.page_size = 5
    queryset = paginator.paginate_queryset(filterset.qs, request)

    serializer = DoctorListSerializer(queryset, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(["GET"])
def doctor_detail(request, pk):
    queryset = DoctorProfile.objects.get(id=pk)
    serializer = DoctorProfileSerializer(queryset)
    return Response(serializer.data)



@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_all_booking(request):
    queryset = DoctorBooking.objects.filter(doctor=request.user)
    serializer = DoctorReadBookingSerializer(queryset, many=True)
    return Response(serializer.data)
