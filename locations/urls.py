from django.urls import path, include
from rest_framework.routers import DefaultRouter

from locations.views import AreaViewSet, CityViewSet, StateViewSet


router = DefaultRouter()
router.register(r"states", StateViewSet, basename="state")
router.register(r"cities", CityViewSet, basename="city")
router.register(r"areas", AreaViewSet, basename="area")

urlpatterns = [
    path("", include(router.urls)),
]
