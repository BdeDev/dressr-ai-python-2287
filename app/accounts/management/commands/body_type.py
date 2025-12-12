from django.core.management.base import BaseCommand
from django.conf import settings
from accounts.models import *
from .default_data import default_body_types
from pathlib import Path
from django.core.files import File

class Command(BaseCommand):
    help = "Seed default body types with icons"

    def handle(self, *args, **options):
        base_icon_path = Path("media/body_icons")
        for item in default_body_types:
            name = item["name"]
            description = item["description"]

            icon_filename = name.lower().replace(" ", "_") + ".svg"
            icon_path = base_icon_path / icon_filename

            if not icon_path.exists():
                self.stdout.write(self.style.ERROR(f"❌ Icon not found for {name}: {icon_path}"))
                continue

            obj, created = BodyType.objects.get_or_create(
                title=name,
                defaults={
                    "description": description,
                }
            )

            if created:
                with open(icon_path, "rb") as f:
                    obj.icon.save(icon_filename, File(f), save=True)

                self.stdout.write(self.style.SUCCESS(f"✔ Added body type: {name}"))
            else:
                self.stdout.write(self.style.WARNING(f"⚠ Already exists: {name}"))

        self.stdout.write(self.style.SUCCESS("🎉 Body Type seeding complete."))