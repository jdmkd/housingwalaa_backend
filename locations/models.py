from django.db import models
from django.core.validators import FileExtensionValidator

# class Location(models.Model):
#     city = models.CharField(max_length=100)
#     state = models.CharField(max_length=100)
#     country = models.CharField(max_length=100)
#     area_name = models.CharField(max_length=150, null=True, blank=True)
#     latitude = models.FloatField(null=True, blank=True)
#     longitude = models.FloatField(null=True, blank=True)

#     def __str__(self):
#         return f"{self.area_name}, {self.city}"

class State(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Gujarat, Maharashtra, etc.

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="housingwalaa/cities/", null=True, blank=True, validators=[FileExtensionValidator(allowed_extensions=['jpg','jpeg','png'])])
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="cities")

    class Meta:
        unique_together = ("name", "state")

    def __str__(self):
        return f"{self.name}, {self.state.name}"


class Area(models.Model):  # Sub-locality / Neighborhood
    name = models.CharField(max_length=150)  # e.g. Satellite, Chandkheda
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="areas")

    class Meta:
        unique_together = ("name", "city")

    def __str__(self):
        return f"{self.name}, {self.city.name}"