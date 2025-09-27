from django.db import models
from accounts.models import User
from locations.models import Location

class Property(models.Model):
    PROPERTY_TYPES = [("RESIDENTIAL", "Residential"), ("COMMERCIAL", "Commercial"), ("PLOT", "Plot")]
    STATUS_CHOICES = [("UNDER_CONSTRUCTION", "Under Construction"), ("READY", "Ready to Move"), ("UPCOMING", "Upcoming")]

    title = models.CharField(max_length=200)
    description = models.TextField()
    property_type = models.CharField(max_length=30, choices=PROPERTY_TYPES)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="properties")
    listed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listed_properties")
    possession_date = models.DateField(null=True, blank=True)
    rera_number = models.CharField(max_length=100, null=True, blank=True)
    price_min = models.DecimalField(max_digits=15, decimal_places=2)
    price_max = models.DecimalField(max_digits=15, decimal_places=2)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class PropertyMedia(models.Model):
    MEDIA_TYPES = [("IMAGE", "Image"), ("FLOORPLAN", "Floorplan"), ("VIDEO", "Video")]

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="media")
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPES)
    file = models.ImageField(upload_to="property/media/", null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.property.title} - {self.media_type}"


class UnitPlan(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="units")
    unit_type = models.CharField(max_length=50)
    size_sqft = models.IntegerField()
    price = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.unit_type} - {self.property.title}"


class Amenity(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=200, null=True, blank=True)
    properties = models.ManyToManyField(Property, related_name="amenities", blank=True)

    def __str__(self):
        return self.name


class Specification(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="specifications")
    category = models.CharField(max_length=100)
    detail = models.TextField()

    def __str__(self):
        return f"{self.property.title} - {self.category}"
