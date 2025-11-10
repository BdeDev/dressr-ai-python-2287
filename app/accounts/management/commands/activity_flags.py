from django.core.management.base import BaseCommand
from wardrobe.models import *
from .default_data import default_activity_flags

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