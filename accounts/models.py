from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from datetime import timedelta
from django.utils import timezone
import random


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)  # admin login
    full_name = models.CharField(max_length=255, blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)

    phone_regex = RegexValidator(
        regex=r'^\+?\d{10,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=15,
        unique=True,
        null=True,
        blank=False
    )

    is_verified = models.BooleanField(default=False)
    
    first_name = None
    last_name = None
    # email = None

    USERNAME_FIELD = "username"   # admin login field
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.username if self.username else str(self.phone_number) or "Unnamed User"


class OTP(models.Model):
    phone_number = models.CharField(max_length=15, db_index=True)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    
    is_used = models.BooleanField(default=False)

    def is_valid(self):
        return not self.is_used and timezone.now() < self.created_at + timedelta(minutes=5)
    
    @staticmethod
    def generate_otp():
        return str(random.randint(100000, 999999))

    def __str__(self):
        return f"{self.phone_number} - {self.code}"
