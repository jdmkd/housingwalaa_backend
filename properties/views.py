from rest_framework import viewsets
from .models import Property, PropertyMedia, UnitPlan, Amenity, Specification
from .serializers import PropertySerializer, PropertyMediaSerializer, UnitPlanSerializer, AmenitySerializer, SpecificationSerializer

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all().select_related("location", "listed_by").prefetch_related("media", "units", "amenities", "specifications")
    serializer_class = PropertySerializer

class PropertyMediaViewSet(viewsets.ModelViewSet):
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
