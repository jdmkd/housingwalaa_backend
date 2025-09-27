from django.contrib import admin
from .models import Promotion

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active")
    search_fields = ("title",)
    list_filter = ("is_active",)
