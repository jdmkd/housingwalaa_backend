from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms
from .models import User, OTP

class CustomUserCreationForm(UserCreationForm):
    """Custom form for creating users in admin (superusers/staff)"""

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")  # no phone number required


class CustomUserChangeForm(UserChangeForm):
    """Custom form for updating users in admin"""

    class Meta:
        model = User
        fields = ("username", "email", "phone_number", "full_name", "is_active", "is_staff", "is_superuser", "is_verified")


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("full_name", "phone_number", "email", "is_verified")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    readonly_fields = ("last_login", "date_joined")
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("username", "email", "password1", "password2")}),
    )
    list_display = ("id", "username", "phone_number", "full_name", "is_staff", "is_superuser", "is_active", "is_verified")
    search_fields = ("username", "phone_number", "full_name", "email")
    ordering = ("id",)


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "code", "created_at", "is_used")
    search_fields = ("phone_number", "code")
    list_filter = ("is_used", "created_at")
