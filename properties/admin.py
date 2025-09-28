from django import forms
from django.contrib import admin
from django.db import models
from django.utils.safestring import mark_safe
from .models import Property, PropertyMedia, UnitPlan, Amenity, Specification

# Inlines for related models
class PropertyMediaInline(admin.TabularInline):
    model = PropertyMedia
    extra = 1
    fields = ("media_type", "file", "video_url", "is_primary")

class UnitPlanInline(admin.TabularInline):
    model = UnitPlan
    extra = 1
    fields = ("unit_type", "size_sqft", "price")

class SpecificationInline(admin.TabularInline):
    model = Specification
    extra = 1
    fields = ("category", "detail")


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["amenities"].label_from_instance = lambda obj: (
            f"{obj.category} - {obj.name}"
        )



# ===== Property Admin =====
@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    exclude = ('created_at',)
    list_display = (
        "title", "property_type", "status", "location",
        "listed_by", "price_range", "is_featured",
    )
    search_fields = ("title", "description", "rera_number")
    list_filter = ("property_type", "status", "is_featured")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("amenities",)  # dual chooser
    inlines = [PropertyMediaInline, UnitPlanInline, SpecificationInline]

    # Format price display
    def price_range(self, obj):
        return f"{obj.price_min} - {obj.price_max}"
    price_range.short_description = "Price Range"


# ===== Amenity Admin =====
@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ("name", "icon", "category")
    search_fields = ("name", "icon", "category")
    # M2M with Property is direct here, so filter_horizontal works

# ===== Optional: Other related models separately =====
@admin.register(PropertyMedia)
class PropertyMediaAdmin(admin.ModelAdmin):
    list_display = ("property", "media_type", "is_primary")

@admin.register(UnitPlan)
class UnitPlanAdmin(admin.ModelAdmin):
    list_display = ("property", "unit_type", "size_sqft", "price")

@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = ("property", "category")