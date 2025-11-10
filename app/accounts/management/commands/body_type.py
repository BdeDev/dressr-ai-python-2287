from django.core.management.base import BaseCommand
from django.conf import settings
from accounts.models import *
from .default_data import default_body_types


class Command(BaseCommand):
    help = "Adding defaut body type"
    def handle(self, *args, **options):
        for type in default_body_types:
            obj, created = BodyType.objects.get_or_create(
                title=type["name"],
                defaults={
                    "description": type["description"],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added body type: {type['name']}"))
            else:
                self.stdout.write(self.style.ERROR(f"Body Type already exists: {type['name']}"))

        self.stdout.write(self.style.SUCCESS(f"Body Type seeding complete."))