from django.core.management.base import BaseCommand
from django.conf import settings
from accounts.models import *

default_hair_colors = [
    {"name": "Black", "hex": "#1C1C1C"},
    {"name": "Dark Brown", "hex": "#4B3621"},
    {"name": "Medium Brown", "hex": "#6B4226"},
    {"name": "Light Brown", "hex": "#8B5A2B"},
    {"name": "Chestnut", "hex": "#954535"},
    {"name": "Auburn", "hex": "#A52A2A"},
    {"name": "Dark Blonde", "hex": "#C19A6B"},
    {"name": "Blonde", "hex": "#F2D16B"},
    {"name": "Light Blonde", "hex": "#FAE7B5"},
    {"name": "Platinum Blonde", "hex": "#F9F6EE"},
    {"name": "Gray", "hex": "#A0A0A0"},
    {"name": "White", "hex": "#FFFFFF"}
]

class Command(BaseCommand):
    help = "Adding defaut skin tone"
    def handle(self, *args, **options):
        for color in default_hair_colors:
            obj, created = HairColor.objects.get_or_create(
                title=color["name"],
                defaults={
                    "color_code": color["hex"],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added hair color: {color['name']}"))
            else:
                self.stdout.write(self.style.ERROR(f"Hair color already exists: {color['name']}"))

        self.stdout.write(self.style.SUCCESS(f"Hair color seeding complete."))