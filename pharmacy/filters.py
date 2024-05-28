import django_filters
from .models import Pharmacy, Product, Medicine


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Product
        fields = ["name"]


class MedicineFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    category = django_filters.CharFilter(lookup_expr="icontains")
    subcategory = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Medicine
        fields = ["name", "category", "subcategory"]


class DeviceFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    category = django_filters.CharFilter(lookup_expr="icontains")
    subcategory = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Medicine
        fields = ["name", "category", "subcategory"]



class PharmacyFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    rating = django_filters.NumberFilter(field_name="rating", lookup_expr="gte")

    class Meta:
        model = Pharmacy
        fields = ["name", "rating"]