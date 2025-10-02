from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from properties.filters import PropertyFilter
from core.permissions import IsAuthenticatedOrReadOnly
from .models import Developer, NearbyPlace, Property, PropertyDetails, PropertyMedia, RateCard, UnitPlan, Amenity, Specification
from .serializers import DeveloperSerializer, NearbyPlaceSerializer, PropertyDetailsSerializer, PropertyListSerializer, PropertySerializer, PropertyMediaSerializer, RateCardSerializer, UnitPlanSerializer, AmenitySerializer, SpecificationSerializer
from rest_framework import generics, status, permissions, throttling
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from core.response_utils import success_response, error_response

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all().prefetch_related(
        "media", "units", "amenities", "specifications", "rate_cards", "nearby_places"
    ).select_related("developer", "area", "listed_by")
    
    # permission_classes = [permissions.AllowAny]
    permission_classes = [IsAuthenticatedOrReadOnly]

    http_method_names = ["get", "head", "options"]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        "title",
        "description",
        "slug",
        "area__name",
        "developer__name",
        "address_line1",
        "address_line2",
        "pincode",
    ]
    filterset_class = PropertyFilter
    # filterset_fields = ["property_type", "status", "area"]
    ordering_fields = ["created_at", "title", "price_min", "price_max"]
    ordering = ["-created_at", "id"]
    
    def get_serializer_class(self):
        if self.action == "list":
            return PropertyListSerializer  # lightweight for listing
        return PropertySerializer  # full details for retrieve, create, update, etc.

    def retrieve(self, request, *args, **kwargs):
        # Support /properties/{slug}/ or /properties/{id}/ transparently
        lookup_value = kwargs.get(self.lookup_field or "pk") or kwargs.get("pk")
        queryset = self.get_queryset()

        obj = None
        if lookup_value is not None:
            # Try slug first (even if numeric-like)
            obj = queryset.filter(slug=lookup_value).first()
            # Fallback to ID if numeric
            if obj is None and str(lookup_value).isdigit():
                obj = queryset.filter(id=int(lookup_value)).first()

        if obj is None:
            # Default behavior (may 404 if not a valid pk)
            response = super().retrieve(request, *args, **kwargs)
            # Wrap default response if successful
            if response.status_code == 200:
                return success_response(data=response.data)
            return response

        serializer = PropertySerializer(obj, context={"request": request})
        return success_response(data=serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)

            # Build pagination metadata if paginator is PageNumberPagination-like
            pagination_meta = None
            paginator = getattr(self, 'paginator', None)
            if paginator is not None:
                try:
                    pagination_meta = {
                        "count": paginator.page.paginator.count,
                        "page": paginator.page.number,
                        "page_size": paginator.get_page_size(request),
                        "total_pages": paginator.page.paginator.num_pages,
                        "next": paginator.get_next_link(),
                        "previous": paginator.get_previous_link(),
                    }
                except Exception:
                    # Fallback minimal pagination data
                    pagination_meta = {
                        "next": paginator.get_next_link() if hasattr(paginator, 'get_next_link') else None,
                        "previous": paginator.get_previous_link() if hasattr(paginator, 'get_previous_link') else None,
                    }

            return success_response(data=serializer.data, pagination=pagination_meta)

        serializer = self.get_serializer(queryset, many=True)
        return success_response(data=serializer.data)

class PropertyMediaViewSet(viewsets.ModelViewSet):
    # queryset = Property.objects.all().select_related("area", "listed_by").prefetch_related("media", "units", "amenities", "specifications")
    # serializer_class = PropertySerializer
    # filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # filterset_fields = ["property_type", "status", "area", "is_featured"]
    # search_fields = ["title", "description", "area__name"]
    # ordering_fields = ["price_min", "price_max", "created_at"]

    queryset = PropertyMedia.objects.all()
    serializer_class = PropertyMediaSerializer

class UnitPlanViewSet(viewsets.ModelViewSet):
    queryset = UnitPlan.objects.all()
    serializer_class = UnitPlanSerializer

class AmenityViewSet(viewsets.ModelViewSet):
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer

class SpecificationViewSet(viewsets.ModelViewSet):
    queryset = Specification.objects.all()
    serializer_class = SpecificationSerializer

class PropertyDetailsViewSet(viewsets.ModelViewSet):
    queryset = PropertyDetails.objects.all()
    serializer_class = PropertyDetailsSerializer

class RateCardViewSet(viewsets.ModelViewSet):
    queryset = RateCard.objects.all()
    serializer_class = RateCardSerializer


class NearbyPlaceViewSet(viewsets.ModelViewSet):
    queryset = NearbyPlace.objects.all()
    serializer_class = NearbyPlaceSerializer


class DeveloperViewSet(viewsets.ModelViewSet):
    queryset = Developer.objects.all()
    serializer_class = DeveloperSerializer