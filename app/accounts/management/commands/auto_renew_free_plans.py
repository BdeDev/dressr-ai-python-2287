from django.core.management.base import BaseCommand
from subscription.models import SubscriptionPlans, UserPlanPurchased
from dateutil.relativedelta import relativedelta
from datetime import datetime
from accounts.constants import *

class Command(BaseCommand):
    help = "Auto renew expired free subscriptions"

    def handle(self, *args, **kwargs):
        now = datetime.now()

        free_plan = SubscriptionPlans.objects.filter(is_free_plan=True).first()
        if not free_plan:
            self.stdout.write("No free plan found")
            return

        expired_plans = UserPlanPurchased.objects.filter(
            subscription_plan=free_plan,
            expire_on__lt=now
        )

        for plan in expired_plans:
            plan.status = USER_PLAN_ACTIVE
            plan.activated_on = now

            if plan.validity == MONTHLY_PLAN:
                plan.expire_on = now + relativedelta(months=plan.month_year)
            elif plan.validity == YEARLY_PLAN:
                plan.expire_on = now + relativedelta(years=plan.month_year)

            plan.renewable_count += 1

            plan.save()

        self.stdout.write(
            self.style.SUCCESS(f"Renewed free subscriptions")
        )
