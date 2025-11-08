from django.core.management.base import BaseCommand
from django.conf import settings
from accounts.models import *
from .default_data import default_skin_tones



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
