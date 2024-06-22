# django imports
from django_filters import rest_framework as filters
# internal imports
from accounts.models import DoctorProfile
from .models import DoctorBooking


class DoctorFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="user__full_name", lookup_expr="icontains")
    rating = filters.NumberFilter(field_name="rating", lookup_expr="gte")
    specialization = filters.CharFilter(
        field_name="specialization", lookup_expr="icontains"
    )
    class Meta:
        model = DoctorProfile
        fields = ["name", "rating", "specialization"]


class DoctorBookingFilter(filters.FilterSet):
    class Meta:
        model = DoctorBooking
        fields = {
            "status": ["exact"],
        }
