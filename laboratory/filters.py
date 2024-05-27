from django_filters import rest_framework as filters
from .models import Laboratory
from .models import LabBooking


class LaboratoryFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")
    technology = filters.CharFilter(lookup_expr="icontains")
    # minPrice = django_filters.filters.CharFilter(field_name='price' or 0,lookup_expr='gte')
    rate = filters.filters.CharFilter(field_name="rate" or 5, lookup_expr="gte")

    class Meta:
        model = Laboratory
        fields = ["name", "technology", "rate"]



class LabBookingFilter(filters.FilterSet):
    class Meta:
        model = LabBooking
        fields = {
            "status": ["exact"],
        }
