from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PropertyViewSet, PropertyMediaViewSet, UnitPlanViewSet, AmenityViewSet, SpecificationViewSet

router = DefaultRouter()
router.register(r"", PropertyViewSet, basename="property")
router.register("media", PropertyMediaViewSet, basename="property-media")
router.register("units", UnitPlanViewSet, basename="unit-plan")
router.register("amenities", AmenityViewSet, basename="amenity")
router.register("specifications", SpecificationViewSet, basename="specification")

urlpatterns = [
    path("", include(router.urls)),
]
