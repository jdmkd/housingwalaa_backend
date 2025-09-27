from django.contrib import admin
from .models import Location

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("area_name", "city", "state", "country")
    search_fields = ("area_name", "city", "state")
