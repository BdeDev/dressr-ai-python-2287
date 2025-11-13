from django.core.management.base import BaseCommand
from django.conf import settings
from accounts.models import *
from .default_data import default_hair_colors


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