import django_filters
from .models import Property

class PropertyFilter(django_filters.FilterSet):
    # Exact matches
    property_type = django_filters.CharFilter(field_name="property_type", lookup_expr="iexact")
    status = django_filters.CharFilter(field_name="status", lookup_expr="iexact")
    location = django_filters.NumberFilter(field_name="location__id")  # filter by location ID

    # Range filters
    price_min = django_filters.NumberFilter(field_name="price_min", lookup_expr="gte")
    price_max = django_filters.NumberFilter(field_name="price_max", lookup_expr="lte")

    class Meta:
        model = Property
        fields = ["property_type", "status", "location", "price_min", "price_max"]
