from django_filters import rest_framework as filters
from accounts.models import DoctorProfile


class DoctorFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="user__first_name", lookup_expr="icontains")
    min_rating = filters.NumberFilter(field_name="rating", lookup_expr="gte")
    max_rating = filters.NumberFilter(field_name="rating", lookup_expr="lte")

    class Meta:
        model = DoctorProfile
        fields = ['name', 'min_rating', 'max_rating']
