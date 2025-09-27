from django.db import models
from accounts.models import User
from properties.models import Property

class Inquiry(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="inquiries")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="inquiries")
    message = models.TextField(null=True, blank=True)
    contact_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inquiry by {self.user.username} on {self.property.title}"
