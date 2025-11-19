from django.core.management.base import BaseCommand
from accounts.models import User
from accounts.constants import *
from subscription.models import SubscriptionPlans
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
                user = User.objects.filter(role_id=ADMIN,is_superuser=True)
                title = 'Free Plan'
                month_year = 1
                validity = 1
                price = 0.00
                final_price = price * (month_year * 12)
                final_price = round(final_price,2)

                if SubscriptionPlans.objects.filter(validity=validity,month_year=month_year,is_deleted=False,is_free_plan=True).exists():
                    self.stdout.write(self.style.SUCCESS('Subscription plan already exist !'))
            
                plan = SubscriptionPlans.objects.create(
                    title = title,
                    month_year = month_year,
                    validity = validity,
                    features = 'Free Plan',
                    price = price,
                    final_price = final_price,
                    created_by = user,
                    status = False,
                    max_uploads = 10,
                    max_try_ons = 10,
                    max_shares = 10,
                    is_free_plan = True
                )
            except Exception as e:
                self.stdout.write(self.style.ERROR(e))
                return None
            self.stdout.write(self.style.SUCCESS('Subscription plan added successfully!'))