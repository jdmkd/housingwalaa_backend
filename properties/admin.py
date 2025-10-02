from django import forms
from django.contrib import admin
from django.db import models
from django.utils.safestring import mark_safe
from .models import Developer, NearbyPlace, Property, PropertyDetails, PropertyMedia, RateCard, UnitPlan, Amenity, Specification

# Inlines for related models
class PropertyMediaInline(admin.TabularInline):
    model = PropertyMedia
    extra = 1
    fields = ("media_type", "file", "video_url", "virtual_tour_url", "is_primary")

class UnitPlanInline(admin.TabularInline):
    model = UnitPlan
    extra = 1
    fields = (
        "unit_type", "rooms", "bathrooms", "balconies",
        "carpet_area_sqft", "builtup_area_sqft", "super_builtup_area_sqft",
        "price", "price_per_sqft", "floor_plan_image",
    )

class SpecificationInline(admin.TabularInline):
    model = Specification
    extra = 1
    fields = ("category", "detail")

class RateCardInline(admin.TabularInline):
    model = RateCard
    extra = 1
    fields = ("name", "amount", "unit")

class NearbyPlaceInline(admin.TabularInline):
    model = NearbyPlace
    extra = 1
    fields = ("name", "distance_km", "travel_time_min")

# class PropertyDetailsInline(admin.StackedInline):
#     model = PropertyDetails
#     extra = 0
#     can_delete = False

class PropertyDetailsInline(admin.StackedInline):
    model = PropertyDetails
    extra = 0
    can_delete = False
    fieldsets = (
        ("Project Info", {
            "fields": (
                "total_towers", "total_units", "floors",
                "project_size_acres", "plot_area_acres", "construction_area_acres", "open_area_percentage",
            )
        }),
        ("Location & Parking", {
            "fields": (
                "parking_type", "facing", "project_position", "road_connectivity",
            )
        }),
        ("Other Info", {
            "fields": (
                "approved_banks", "current_status", "last_updated",
            )
        }),
    )

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Show category + name in the amenity chooser
        self.fields["amenities"].label_from_instance = lambda obj: (
            f"{obj.category} - {obj.name}" if obj.category else obj.name
        )



# ===== Property Admin =====
@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    # form = PropertyForm
    exclude = ('created_at',)
    list_display = (
        "title", "property_type", "status",
        "listed_by", "price_range", "is_featured", "developer",
    )
    search_fields = ("title", "description", "area__name", "rera_number", "developer__name")
    list_filter = ("property_type", "status", "is_featured", "area", "developer")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("amenities",)  # dual chooser
    
    inlines = [
        PropertyDetailsInline,
        PropertyMediaInline,
        UnitPlanInline,
        SpecificationInline,
        RateCardInline,
        NearbyPlaceInline,
    ]

    # Format price display
    def price_range(self, obj):
        return f"{obj.price_min} - {obj.price_max}"
    price_range.short_description = "Price Range"


# ========== Developer Admin ==========
class PropertyInline(admin.TabularInline):
    model = Property
    fields = ("title", "property_type", "status", "is_featured", "price_min", "price_max")
    extra = 1
    show_change_link = True

# ========= Developer Admin =========
@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    list_display = ("name", "website", "contact_number")
    search_fields = ("name", "website", "contact_number")
    inlines = [PropertyInline]

# ===== Amenity Admin =====
@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ("name", "icon", "category")
    search_fields = ("name", "icon", "category")

# ===== Optional: Other related models separately =====
@admin.register(PropertyMedia)
class PropertyMediaAdmin(admin.ModelAdmin):
    list_display = ("property", "media_type", "is_primary")

@admin.register(UnitPlan)
class UnitPlanAdmin(admin.ModelAdmin):
    list_display = (
        "property", "unit_type", "rooms", "bathrooms",
        "balconies", "price", "price_per_sqft",
    )

@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = ("property", "category")

@admin.register(PropertyDetails)
class PropertyDetailsAdmin(admin.ModelAdmin):
    list_display = ("property", "total_towers", "total_units", "floors", "project_size_acres")

# ========= RateCard Admin =========
@admin.register(RateCard)
class RateCardAdmin(admin.ModelAdmin):
    list_display = ("property", "name", "amount", "unit")


# ========= NearbyPlace Admin =========
@admin.register(NearbyPlace)
class NearbyPlaceAdmin(admin.ModelAdmin):
    list_display = ("property", "name", "distance_km", "travel_time_min")