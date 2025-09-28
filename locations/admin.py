from django.contrib import admin
from .models import Location

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("city", "area_name", "state", "country")
    search_fields = ("city", "state", "area_name")
