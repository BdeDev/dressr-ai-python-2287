from django.core.management.base import BaseCommand
from wardrobe.models import ClothCategory
from .default_data import ACTIVITY_ITEM_MAP



class Command(BaseCommand):
    help = "Seed default cloth categories based on activity items"

    def handle(self, *args, **options):
        created_count = 0
        existing_count = 0

        for activity, items in ACTIVITY_ITEM_MAP.items():
            for item in items:

                title = item.replace("_", " ").title()

                obj, created = ClothCategory.objects.get_or_create(
                    title=title
                )

                if created:
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(f"Added cloth category: {title}"))
                else:
                    existing_count += 1
                    self.stdout.write(self.style.WARNING(f"Cloth category exists: {title}"))

        self.stdout.write(self.style.SUCCESS(
            f"Seeding complete. Added: {created_count}, Existing: {existing_count}"
        ))

