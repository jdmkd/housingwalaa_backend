from rest_framework import viewsets

from core.permissions import IsAuthenticatedOrReadOnly
from .models import State, City, Area
from .serializers import StateSerializer, CitySerializer, AreaSerializer


class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.all().order_by("name")
    serializer_class = StateSerializer
    # permission_classes = [permissions.AllowAny]
    permission_classes = [IsAuthenticatedOrReadOnly]


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.select_related("state").all().order_by("name")
    serializer_class = CitySerializer
    # permission_classes = [permissions.AllowAny]
    permission_classes = [IsAuthenticatedOrReadOnly]

class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.select_related("city", "city__state").all().order_by("name")
    serializer_class = AreaSerializer
    # permission_classes = [permissions.AllowAny]
    permission_classes = [IsAuthenticatedOrReadOnly]