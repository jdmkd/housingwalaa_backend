from rest_framework import viewsets

from properties.filters import PropertyFilter
from properties.permissions import IsAuthenticatedOrReadOnlyForPOST
from .models import Property, PropertyMedia, UnitPlan, Amenity, Specification
from .serializers import PropertyListSerializer, PropertySerializer, PropertyMediaSerializer, UnitPlanSerializer, AmenitySerializer, SpecificationSerializer
from rest_framework import generics, status, permissions, throttling
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all().prefetch_related("media", "units", "amenities", "specifications")
    # serializer_class = PropertySerializer  # it returns full details of the property data.
    serializer_class = PropertyListSerializer  # it returns a lightweight version of the property data.

    permission_classes = [permissions.AllowAny]
    # permission_classes = [IsAuthenticatedOrReadOnlyForPOST]

    filter_backends = [DjangoFilterBackend]
    filterset_class = PropertyFilter
    # filterset_fields = ["property_type", "status", "location"]
    ordering_fields = ["price_min", "price_max", "created_at"]
    ordering = ["-created_at"]
    
    def get_serializer_class(self):
        if self.action == "list":
            return PropertyListSerializer  # lightweight for listing
        return PropertySerializer  # full details for retrieve, create, update, etc.

class PropertyMediaViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all().select_related("location", "listed_by").prefetch_related("media", "units", "amenities", "specifications")
    serializer_class = PropertySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["property_type", "status", "location", "is_featured"]
    search_fields = ["title", "description", "location__name"]
    ordering_fields = ["price_min", "price_max", "created_at"]

class UnitPlanViewSet(viewsets.ModelViewSet):
    queryset = UnitPlan.objects.all()
    serializer_class = UnitPlanSerializer

class AmenityViewSet(viewsets.ModelViewSet):
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer

class SpecificationViewSet(viewsets.ModelViewSet):
    queryset = Specification.objects.all()
    serializer_class = SpecificationSerializer
