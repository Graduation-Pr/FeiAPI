import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    category = django_filters.CharFilter(lookup_expr="icontains")
    subcategory = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Product
        fields = ["name", "category", "subcategory"]
