from rest_framework import serializers
from .models import Property, PropertyMedia, UnitPlan, Amenity, Specification

class PropertyMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyMedia
        fields = "__all__"

class UnitPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitPlan
        fields = "__all__"

class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = "__all__"

class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = "__all__"

class PropertySerializer(serializers.ModelSerializer):
    media = PropertyMediaSerializer(many=True, read_only=True)
    units = UnitPlanSerializer(many=True, read_only=True)
    specifications = SpecificationSerializer(many=True, read_only=True)
    amenities = AmenitySerializer(many=True, read_only=True)

    class Meta:
        model = Property
        fields = "__all__"
