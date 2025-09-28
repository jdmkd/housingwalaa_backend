from django.core.management.base import BaseCommand
from properties.models import Amenity

class Command(BaseCommand):
    help = "Seed the database with common real estate amenities, including icons and categories"

    def handle(self, *args, **kwargs):
        amenities = [
            # Indoor / Unit-level
            {"name": "Air Conditioning", "icon": "fa-snowflake", "category": "Indoor"},
            {"name": "Heating", "icon": "fa-fire", "category": "Indoor"},
            {"name": "Ceiling Fans", "icon": "fa-fan", "category": "Indoor"},
            {"name": "High-speed Internet", "icon": "fa-wifi", "category": "Indoor"},
            {"name": "Cable TV", "icon": "fa-tv", "category": "Indoor"},
            {"name": "Modular Kitchen", "icon": "fa-kitchen-set", "category": "Indoor"},
            {"name": "Wardrobes / Built-in Closets", "icon": "fa-closet", "category": "Indoor"},
            {"name": "Smart Home Features", "icon": "fa-microchip", "category": "Indoor"},
            {"name": "Laundry / Washer & Dryer", "icon": "fa-tshirt", "category": "Indoor"},
            {"name": "Fireplace", "icon": "fa-fireplace", "category": "Indoor"},

            # Outdoor / Community
            {"name": "Swimming Pool", "icon": "fa-swimmer", "category": "Outdoor"},
            {"name": "Gym / Fitness Center", "icon": "fa-dumbbell", "category": "Outdoor"},
            {"name": "Clubhouse / Community Hall", "icon": "fa-building", "category": "Outdoor"},
            {"name": "Playground / Kids’ Area", "icon": "fa-child", "category": "Outdoor"},
            {"name": "Landscaped Garden", "icon": "fa-tree", "category": "Outdoor"},
            {"name": "Jogging / Walking Tracks", "icon": "fa-person-running", "category": "Outdoor"},
            {"name": "Tennis Court", "icon": "fa-table-tennis", "category": "Outdoor"},
            {"name": "Basketball Court", "icon": "fa-basketball", "category": "Outdoor"},
            {"name": "BBQ / Picnic Area", "icon": "fa-bbq", "category": "Outdoor"},
            {"name": "Parking", "icon": "fa-parking", "category": "Outdoor"},
            {"name": "Security / CCTV", "icon": "fa-camera", "category": "Outdoor"},
            {"name": "Elevators / Lifts", "icon": "fa-elevator", "category": "Outdoor"},

            # Safety & Convenience
            {"name": "Fire Alarms / Sprinklers", "icon": "fa-bell", "category": "Safety"},
            {"name": "24/7 Security", "icon": "fa-shield-alt", "category": "Safety"},
            {"name": "Backup Power / Generator", "icon": "fa-bolt", "category": "Safety"},
            {"name": "Water Supply / Storage Tanks", "icon": "fa-water", "category": "Safety"},
            {"name": "Waste Disposal / Recycling", "icon": "fa-recycle", "category": "Safety"},

            # Luxury / Premium
            {"name": "Spa / Sauna / Jacuzzi", "icon": "fa-hot-tub", "category": "Luxury"},
            {"name": "Golf Course", "icon": "fa-golf-ball", "category": "Luxury"},
            {"name": "Rooftop Terrace", "icon": "fa-building-roof", "category": "Luxury"},
            {"name": "Concierge Services", "icon": "fa-concierge-bell", "category": "Luxury"},
            {"name": "Private Cinema / Theatre Room", "icon": "fa-film", "category": "Luxury"},
            {"name": "Smart Home Automation", "icon": "fa-lightbulb", "category": "Luxury"},
            {"name": "Pet-friendly Facilities", "icon": "fa-dog", "category": "Luxury"},
            {"name": "EV Charging", "icon": "fa-charging-station", "category": "Luxury"},
        ]

        created_count = 0
        for amenity in amenities:
            obj, created = Amenity.objects.get_or_create(
                name=amenity["name"],
                defaults={
                    "icon": amenity["icon"],
                    "category": amenity["category"]  # make sure Amenity model has 'category' field
                }
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f"Seeded {created_count} amenities successfully."))
