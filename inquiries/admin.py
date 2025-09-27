from django.contrib import admin
from .models import Inquiry

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ("property", "user", "contact_number", "created_at")
    search_fields = ("property__title", "user__username", "contact_number")
