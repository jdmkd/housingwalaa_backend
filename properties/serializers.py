from rest_framework import serializers
from .models import Developer, NearbyPlace, Property, PropertyDetails, PropertyMedia, RateCard, UnitPlan, Amenity, Specification

class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ("id", "name", "icon", "category")

class PropertyMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyMedia
        fields = [
            "id", "media_type", "file", "video_url", "virtual_tour_url", 
            "is_primary", "property"
        ]

class UnitPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitPlan
        fields = (
            "id", "unit_type", "rooms", "bathrooms", "balconies",
            "carpet_area_sqft", "builtup_area_sqft", "super_builtup_area_sqft",
            "price", "price_per_sqft", "floor_plan_image", "property"
        )

class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = ("id", "category", "detail", "property")

class PropertyDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyDetails
        fields = "__all__"
        extra_kwargs = {
            "property": {"read_only": True}
        }

class RateCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = RateCard
        fields = ("id", "name", "amount", "unit", "property")


class NearbyPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NearbyPlace
        fields = ("id", "name", "distance_km", "travel_time_min", "property")


class DeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Developer
        fields = ("id", "name", "about", "logo", "website", "contact_number")

class PropertyDetailsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyDetails
        fields = (
            "total_towers",
            "total_units",
            "floors",
            "current_status",
        )

class PropertyMediaListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyMedia
        fields = [
            "id", "media_type", "file","is_primary"
        ]

class UnitPlanListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitPlan
        fields = (
            "id", "unit_type",
        )

class PropertyListSerializer(serializers.ModelSerializer):
    developer = DeveloperSerializer(read_only=True)
    area_name = serializers.CharField(source="area.name", read_only=True)
    property_details = PropertyDetailsListSerializer(source="details", read_only=True)
    # property_media = PropertyMediaListSerializer(source="media", many=True, read_only=True)
    property_media = serializers.SerializerMethodField()
    units = UnitPlanListSerializer(many=True, required=False)
    amenities_count = serializers.SerializerMethodField()

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
            "area",
            "area_name",
            "units",
            "property_media",
            "property_details",
            "amenities_count",
            "address_line1",
            "address_line2",
            "pincode",
            "possession_date",
            "developer",
        )
        
    def get_amenities_count(self, obj):
        return obj.amenities.count()
    
    def get_property_media(self, obj):
        images = obj.media.filter(media_type="IMAGE")
        return PropertyMediaListSerializer(images, many=True).data
    

class PropertySerializer(serializers.ModelSerializer):
    amenities = AmenitySerializer(many=True, required=False)
    media = PropertyMediaSerializer(many=True, required=False)
    units = UnitPlanSerializer(many=True, required=False)
    specifications = SpecificationSerializer(many=True, required=False)
    details = PropertyDetailsSerializer(required=False)
    rate_cards = RateCardSerializer(many=True, required=False)
    nearby_places = NearbyPlaceSerializer(many=True, required=False)
    developer = DeveloperSerializer(read_only=True)

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
        details_data = validated_data.pop("details", None)
        rate_cards_data = validated_data.pop("rate_cards", [])
        nearby_places_data = validated_data.pop("nearby_places", [])


        # Create Property
        property_obj = Property.objects.create(**validated_data)

        # Related nested objects
        for m in media_data:
            PropertyMedia.objects.create(property=property_obj, **m)
        for u in units_data:
            UnitPlan.objects.create(property=property_obj, **u)
        for s in specifications_data:
            Specification.objects.create(property=property_obj, **s)
        for r in rate_cards_data:
            RateCard.objects.create(property=property_obj, **r)
        for np in nearby_places_data:
            NearbyPlace.objects.create(property=property_obj, **np)
        
        if details_data:
            PropertyDetails.objects.create(property=property_obj, **details_data)

        # property_obj.amenities.set(amenities_data)
        property_obj.amenities.set([a["id"] for a in amenities_data] if amenities_data else [])

        return property_obj
    

    def update(self, instance, validated_data):
        # Nested updates
        amenities_data = validated_data.pop("amenities", None)
        media_data = validated_data.pop("media", None)
        units_data = validated_data.pop("units", None)
        specifications_data = validated_data.pop("specifications", None)
        details_data = validated_data.pop("details", None)
        rate_cards_data = validated_data.pop("rate_cards", None)
        nearby_places_data = validated_data.pop("nearby_places", None)

        # Update property fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if amenities_data is not None:
            # instance.amenities.set(amenities_data)
            instance.amenities.set([a["id"] for a in amenities_data])


        if details_data:
            PropertyDetails.objects.update_or_create(
                property=instance, defaults=details_data
            )

        return instance