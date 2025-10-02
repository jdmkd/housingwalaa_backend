from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DeveloperViewSet, NearbyPlaceViewSet, PropertyDetailsViewSet, PropertyViewSet, PropertyMediaViewSet, RateCardViewSet, UnitPlanViewSet, AmenityViewSet, SpecificationViewSet

router = DefaultRouter()
router.register(r"", PropertyViewSet, basename="property")
router.register(r"media", PropertyMediaViewSet, basename="property-media")
router.register(r"units", UnitPlanViewSet, basename="unit-plan")
router.register(r"amenities", AmenityViewSet, basename="amenity")
router.register(r"specifications", SpecificationViewSet, basename="specification")
router.register(r"details", PropertyDetailsViewSet, basename="property-details")
router.register(r"rate-cards", RateCardViewSet, basename="rate-card")
router.register(r"nearby-places", NearbyPlaceViewSet, basename="nearby-place")
router.register(r"developers", DeveloperViewSet, basename="developer")

urlpatterns = [
    path("", include(router.urls)),
]
