from django.shortcuts import render
from accounts.models import DoctorProfile, User
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from .filters import DoctorFilter
from rest_framework.pagination import PageNumberPagination
from .serializers import DoctorListSerializer
from rest_framework.response import Response
from rest_framework import generics
from accounts.serializers import DoctorProfileSerializer

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


class DoctorDetail(generics.RetrieveAPIView):
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorProfileSerializer
