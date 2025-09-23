from django.core.management.base import BaseCommand
from accounts.models import User
from accounts.constants import *
import environ

env = environ.Env()
environ.Env.read_env()

class Command(BaseCommand):
    help = "Create super admin"
    def handle(self, *args, **options):
        if User.objects.filter(role_id=ADMIN,is_superuser=True):
            self.stdout.write(self.style.ERROR('Superuser already exists!'))
        else:
            try:
                User.objects.create_superuser(
                    username=env('ADMIN_USERNAME'),
                    email=env('ADMIN_EMAIL'),
                    password=env('ADMIN_PASSWORD')
                )
            except Exception as e:
                self.stdout.write(self.style.ERROR(e))
                return None
            self.stdout.write(self.style.SUCCESS('Superuser created successfully!'))

