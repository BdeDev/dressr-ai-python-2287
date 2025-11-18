import os
import logging
import environ
from accounts.models import *
import time
from backup .models import Backup
from datetime import date
from datetime import datetime, timedelta
from accounts.views import *
from django_db_logger .models import StatusLog
from accounts.constants import *
from subscription.models import *
from logger.models import *
from accounts.utils import *
from celery import shared_task


env = environ.Env()
environ.Env.read_env()
db_logger = logging.getLogger('db')

# @shared_task
def WeeklyDataBaseBackup():
    """
    Create Backup Every Day
    """
    try:
        database = env('DB_NAME')
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        if not os.path.exists(f"{path}/media/backup_files"):
            os.makedirs(f"{path}/media/backup_files")
        name = database + time.strftime('%Y%m%d-%H%M%S') + ".sql"
        file_path = f'{path}/media/backup_files/' + name
        os.system("mysqldump -h " + env('DB_HOST') + " -u " + env('DB_USER') + " -p" + env('DB_PASSWORD') + " " + database + " > " + file_path)
        Backup.objects.create(name = name,size = os.path.getsize(file_path),is_schema = False,backup_file = 'backup_files/'+name)
    except Exception as e:
        db_logger.exception(e)

# @shared_task
def DeleteUnnecessaryData():
    """
    Delete Unnecessary Data
    """
    StatusLog.objects.filter(create_datetime__lt = datetime.now()-timedelta(days=15)).delete()   
    EmailLogger.objects.filter(created_on__lt = datetime.now() - timedelta(days=15)).delete()
    ApplicationCrashLogs.objects.filter(created_on__lt = datetime.now() - timedelta(days=15)).delete()


def SendEmailForSubscriptionPurchase():
    """
    Send Subscription Renewal Reminders
    """
    purchased_subscription = UserPlanPurchased.objects.filter(status=USER_PLAN_ACTIVE).order_by('created_on')
    for subscription in purchased_subscription:
        if not subscription:
            continue
        seven_days_before_expiry = subscription.expire_on - timedelta(days=7)
        today = datetime.now().date()

        if today == seven_days_before_expiry:
            notification_title = "Your Subscription is Expiring Soon"
            notification_description = f"""
            Dear {subscription.purchased_by.full_name.capitalize()}, 

            This is a reminder that your subscription plan **{subscription.subscription_plan.title}** 
            will expire on **{subscription.expire_on.strftime('%d %B %Y')}**.
            
            Please renew your plan to continue enjoying uninterrupted access to all premium features.

            Thank you for being a valued member of MyDressr!

            Team MyDressr.
            """

        # 2. Free Plan Notification (user hasn't upgraded)

        elif subscription.subscription_plan.is_free_plan:
            notification_title = "Upgrade Your Plan for Full Access"
            notification_description = f"""
            Dear {subscription.purchased_by.full_name.capitalize()},

            You are currently using a Free Plan, which includes limited uploads 
            and restricted virtual try-on features.

            Upgrade to a Premium Plan to unlock unlimited wardrobe uploads, 
            AI virtual try-on, and more exciting features.

            Thank you for choosing MyDressr!

            Team MyDressr.
            """

        else:
            continue

        notification_description = notification_description.strip()

        bulk_send_notification(
            created_by=None,
            created_for=[subscription.purchased_by],
            title=notification_title,
            description=notification_description,
            notification_type=SUBSCRIPTION_STATUS_NOTIFICATION,
            obj_id=str(subscription.id)
        )
        bulk_send_user_email(
            None,
            subscription.purchased_by,
            'email_templates/subscription-reminder.html',
            notification_title,
            subscription.purchased_by.email,
            subscription,
            subscription,
            "",
            ""
        )
