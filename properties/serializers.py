from rest_framework import serializers
from .models import Property, PropertyMedia, UnitPlan, Amenity, Specification

class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ("id", "name", "icon", "category")

class PropertyMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyMedia
        fields = ["id", "media_type", "file", "video_url", "is_primary", "property"]

class UnitPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitPlan
        fields = ("id", "unit_type", "size_sqft", "price", "property")

class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = ("id", "category", "detail", "property")


class PropertyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = (
            "id",
            "title",
            "slug",
            "property_type",
            "status",
            "price_min",
            "price_max",
            "is_featured",
            "location",
        )
        
class PropertySerializer(serializers.ModelSerializer):
    amenities = AmenitySerializer(many=True, required=False)
    # amenities = serializers.PrimaryKeyRelatedField(many=True, queryset=Amenity.objects.all(), required=False)

    media = PropertyMediaSerializer(many=True, required=False)
    units = UnitPlanSerializer(many=True, required=False)
    specifications = SpecificationSerializer(many=True, required=False)

    class Meta:
        model = Property
        fields = "__all__"
        read_only_fields = ("listed_by", "created_at")

    def create(self, validated_data):
        # Assign the logged-in user
        validated_data["listed_by"] = self.context["request"].user

        # Pop nested related data
        media_data = validated_data.pop("media", [])
        units_data = validated_data.pop("units", [])
        specifications_data = validated_data.pop("specifications", [])
        amenities_data = validated_data.pop("amenities", [])

        # Create the Property instance
        property_obj = Property.objects.create(**validated_data)

        # Create related nested objects
        for m in media_data:
            PropertyMedia.objects.create(property=property_obj, **m)
        for u in units_data:
            UnitPlan.objects.create(property=property_obj, **u)
        for s in specifications_data:
            Specification.objects.create(property=property_obj, **s)
        
        property_obj.amenities.set(amenities_data)

        return property_obj
    

    def update(self, instance, validated_data):
        # Handle nested updates if needed
        # Here we keep it simple: update Property fields and replace nested M2M
        amenities_data = validated_data.pop("amenities", None)
        media_data = validated_data.pop("media", None)
        units_data = validated_data.pop("units", None)
        specifications_data = validated_data.pop("specifications", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if amenities_data is not None:
            instance.amenities.set(amenities_data)

        # Optional: handle media, units, specifications updates here if needed

        return instance