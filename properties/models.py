from django.db import models
from django.utils.text import slugify
from accounts.models import User
from locations.models import Area


class Developer(models.Model):
    name = models.CharField(max_length=200)
    about = models.TextField(null=True, blank=True)
    logo = models.ImageField(upload_to="housingwalaa/developers/logos/", null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    contact_number = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name

class Amenity(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=200, null=True, blank=True)
    category = models.CharField(max_length=50, null=True, blank=True)
    # properties = models.ManyToManyField(Property, related_name="amenities", blank=True)

    def __str__(self):
        return f"{self.category} - {self.name}"
        # return f"{self.name} ({self.category})" if self.category else self.name


class Property(models.Model):

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    
    developer = models.ForeignKey(Developer, on_delete=models.SET_NULL, null=True, related_name="projects")

    # Link to specific Area (which gives us City → State)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True, related_name="properties")
    
    # Detailed address fields
    address_line1 = models.CharField(max_length=255, null=True, blank=True)  # House / Building
    address_line2 = models.CharField(max_length=255, null=True, blank=True)  # Landmark, etc.
    pincode = models.CharField(max_length=10, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    PROPERTY_TYPES = [
        ("APARTMENT", "Apartment"),
        ("VILLA", "Villa"),
        ("RESIDENTIAL", "Residential"), 
        ("COMMERCIAL", "Commercial"), 
        ("PLOT", "Plot")
    ]
    property_type = models.CharField(max_length=30, choices=PROPERTY_TYPES)
    
    STATUS_CHOICES = [("UNDER_CONSTRUCTION", "Under Construction"), ("READY", "Ready to Move"), ("UPCOMING", "Upcoming")]
    status = models.CharField(max_length=30, choices=STATUS_CHOICES)
    
    # location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="properties")
    
    listed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listed_properties")
    amenities = models.ManyToManyField(Amenity, related_name="properties", blank=True)
    # amenities = models.ManyToManyField("Amenity", related_name="properties", blank=True)

    possession_date = models.DateField(null=True, blank=True)
    rera_number = models.CharField(max_length=100, null=True, blank=True)
    price_min = models.DecimalField(max_digits=15, decimal_places=2)
    price_max = models.DecimalField(max_digits=15, decimal_places=2)
    
    is_featured = models.BooleanField(default=False)
    highlights = models.TextField(null=True, blank=True)  # "Why this project points"
    brochure_pdf = models.FileField(upload_to="brochures/", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created_at", "id"]
        
    def __str__(self):
        return self.title

class PropertyDetails(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE, related_name="details")

    total_towers = models.IntegerField(null=True, blank=True)
    total_units = models.IntegerField(null=True, blank=True)
    floors = models.IntegerField(null=True, blank=True)
    project_size_acres = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    plot_area_acres = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    construction_area_acres = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    open_area_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    parking_type = models.CharField(max_length=200, null=True, blank=True)
    facing = models.CharField(max_length=50, null=True, blank=True)
    project_position = models.CharField(max_length=100, null=True, blank=True)
    road_connectivity = models.CharField(max_length=100, null=True, blank=True)

    approved_banks = models.TextField(null=True, blank=True)  # CSV or JSON list
    current_status = models.CharField(max_length=100, null=True, blank=True)
    last_updated = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Details of {self.property.title}"
    
class PropertyMedia(models.Model):
    MEDIA_TYPES = [
        ("IMAGE", "Image"),
        ("FLOORPLAN", "Floorplan"),
        ("VIDEO", "Video"),
        ("VIRTUAL_TOUR", "Virtual Tour"),
    ]

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="media")
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPES)
    file = models.ImageField(upload_to="housingwalaa/property/media/", null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    virtual_tour_url = models.URLField(null=True, blank=True)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.property.title} - {self.media_type}"


class UnitPlan(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="units")
    unit_type = models.CharField(max_length=50)
    rooms = models.IntegerField(default=0)
    bathrooms = models.IntegerField(default=0)
    balconies = models.IntegerField(default=0)
    
    carpet_area_sqft = models.IntegerField(null=True, blank=True)
    builtup_area_sqft = models.IntegerField(null=True, blank=True)
    super_builtup_area_sqft = models.IntegerField(null=True, blank=True)
    
    price = models.DecimalField(max_digits=15, decimal_places=2)
    price_per_sqft = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    floor_plan_image = models.ImageField(upload_to="housingwalaa/unit_plans/", null=True, blank=True)

    def __str__(self):
        return f"{self.unit_type} - {self.property.title}"



class Specification(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="specifications")
    category = models.CharField(max_length=100)
    detail = models.TextField()

    def __str__(self):
        return f"{self.property.title} - {self.category}"


class RateCard(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="rate_cards")
    name = models.CharField(max_length=100)  # e.g. "PLC Charges", "Stamp Duty"
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    unit = models.CharField(max_length=50, null=True, blank=True)  # e.g. "per sq.ft", "fixed"

    def __str__(self):
        return f"{self.property.title} - {self.name}"

class NearbyPlace(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="nearby_places")
    name = models.CharField(max_length=100)  # e.g. "Metro Station"
    distance_km = models.DecimalField(max_digits=5, decimal_places=2)
    travel_time_min = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.property.title} - {self.name}"