from django.shortcuts import render
from .serializers import LaboratorySerializer, LaboratoryDetailSerializer
from .models import Laboratory
from rest_framework import generics
from .filters import LaboratoryFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_labs(request):
    filterset = LaboratoryFilter(
        request.GET, queryset=Laboratory.objects.all().order_by("id")
    )
    paginator = PageNumberPagination()
    paginator.page_size = 6
    queryset = paginator.paginate_queryset(filterset.qs, request)

    serializer = LaboratorySerializer(queryset, many=True)
    return Response({"labs": serializer.data})


class DetailLaboratory(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Laboratory.objects.all()
    serializer_class = LaboratorySerializer




