import django_filters
from .models import Laboratory


class LaboratoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    technology = django_filters.CharFilter(lookup_expr="icontains")
    # minPrice = django_filters.filters.CharFilter(field_name='price' or 0,lookup_expr='gte')
    rate = django_filters.filters.CharFilter(field_name='rate' or 5,lookup_expr='gte')

    class Meta:
        model = Laboratory
        fields = ["name", "technology", "rate"]
