from django.contrib import admin
from .models import Property, PropertyMedia, UnitPlan, Amenity, Specification

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ("title", "property_type", "status", "price_min", "price_max", "is_featured", "created_at")
    search_fields = ("title", "rera_number")
    list_filter = ("property_type", "status", "is_featured")

@admin.register(PropertyMedia)
class PropertyMediaAdmin(admin.ModelAdmin):
    list_display = ("property", "media_type", "is_primary")

@admin.register(UnitPlan)
class UnitPlanAdmin(admin.ModelAdmin):
    list_display = ("property", "unit_type", "size_sqft", "price")

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = ("property", "category")
