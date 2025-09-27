from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PropertyViewSet, PropertyMediaViewSet, UnitPlanViewSet, AmenityViewSet, SpecificationViewSet

router = DefaultRouter()
router.register("properties", PropertyViewSet)
router.register("media", PropertyMediaViewSet)
router.register("units", UnitPlanViewSet)
router.register("amenities", AmenityViewSet)
router.register("specifications", SpecificationViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
