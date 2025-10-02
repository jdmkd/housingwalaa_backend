from django.contrib import admin
from .models import Area, City, State

# @admin.register(Location)
# class LocationAdmin(admin.ModelAdmin):
#     list_display = ("city", "area_name", "state", "country")
#     search_fields = ("city", "state", "area_name")

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "image", "state")
    list_filter = ("state",)
    search_fields = ("name", "state__name")


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "city")
    list_filter = ("city", "city__state")
    search_fields = ("name", "city__name", "city__state__name")