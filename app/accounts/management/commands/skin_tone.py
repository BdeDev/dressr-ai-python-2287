from django.core.management.base import BaseCommand
from django.conf import settings
from accounts.models import *


default_skin_tones = [
        {"name": "Fair", "hex": "#FFDFC4"},
        {"name": "Very Fair", "hex": "#FFD7A2"},
        {"name": "Light Fair", "hex": "#FFDC8B"},
        {"name": "Light", "hex": "#FFDA82"},
        {"name": "Medium", "hex": "#F0E68C"},
        {"name": "Olive", "hex": "#AD8E39"},
        {"name": "Tan", "hex": "#D2B48C"},
        {"name": "Dark Tan", "hex": "#CD853F"},
        {"name": "Deep Tan", "hex": "#B8860B"},
        {"name": "Dark", "hex": "#8B4513"},
        {"name": "Very Dark", "hex": "#704833"},
        {"name": "Black", "hex": "#000000"}
    ]

class Command(BaseCommand):
    help = "Adding defaut skin tone"
    def handle(self, *args, **options):
        for tone in default_skin_tones:
            obj, created = SkinTone.objects.get_or_create(
                title=tone["name"],
                defaults={
                    "color_code": tone["hex"],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added skin tone: {tone['name']}"))
            else:
                self.stdout.write(self.style.ERROR(f"Skin tone already exists: {tone['name']}"))

        self.stdout.write(self.style.SUCCESS(f"Skin tone seeding complete."))
