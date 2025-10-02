import django_filters
from .models import Property

class PropertyFilter(django_filters.FilterSet):
    # Exact matches
    property_type = django_filters.CharFilter(field_name="property_type", lookup_expr="iexact")
    status = django_filters.CharFilter(field_name="status", lookup_expr="iexact")
    # Slug support
    slug = django_filters.CharFilter(field_name="slug", lookup_expr="iexact")
    # Area/Location support (alias to avoid breaking clients)
    area = django_filters.NumberFilter(field_name="area__id")
    location = django_filters.NumberFilter(field_name="area__id")
    area_name = django_filters.CharFilter(field_name="area__name", lookup_expr="icontains")
    developer = django_filters.NumberFilter(field_name="developer__id")
    developer_name = django_filters.CharFilter(field_name="developer__name", lookup_expr="icontains")

    # Range filters
    price_min = django_filters.NumberFilter(field_name="price_min", lookup_expr="gte")
    price_max = django_filters.NumberFilter(field_name="price_max", lookup_expr="lte")

    # Boolean/flags
    is_featured = django_filters.BooleanFilter(field_name="is_featured")
    status_in = django_filters.BaseInFilter(field_name="status", lookup_expr="in")

    class Meta:
        model = Property
        fields = [
            "property_type",
            "status",
            "status_in",
            "slug",
            "area",
            "location",
            "area_name",
            "developer",
            "developer_name",
            "price_min",
            "price_max",
            "is_featured",
        ]
