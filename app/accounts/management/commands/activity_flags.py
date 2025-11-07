from django.core.management.base import BaseCommand
from wardrobe.models import *


default_activity_flags = [
    {"name": "Swim", "description": "Swimwear and beach essentials"},
    {"name": "Hiking", "description": "Outdoor and hiking gear"},
    {"name": "Formal Meetings", "description": "Formal attire and accessories."},
    {"name": "Night Life", "description": "Party and nightlife outfits."},
    {"name": "Desert", "description": "Desert-specific clothing and gear."},
    {"name": "Other activities", "description": "Additional activities, such as skiing or yoga."},
]
class Command(BaseCommand):
    help = "Adding defaut skin tone"
    def handle(self, *args, **options):
        for activity in default_activity_flags:
            obj, created = ActivityFlag.objects.get_or_create(
                name=activity["name"],
                defaults={
                    "description": activity["description"],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added activity flags: {activity['name']}"))
            else:
                self.stdout.write(self.style.ERROR(f"Hair activity flags exists: {activity['name']}"))

        self.stdout.write(self.style.SUCCESS(f"Activity Flag seeding complete."))