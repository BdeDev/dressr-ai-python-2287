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
from logger.models import *
from celery import shared_task


env = environ.Env()
environ.Env.read_env()
db_logger = logging.getLogger('db')

@shared_task
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

@shared_task
def DeleteUnnecessaryData():
    """
    Delete Unnecessary Data
    """
    StatusLog.objects.filter(create_datetime__lt = datetime.now()-timedelta(days=15)).delete()   
    EmailLogger.objects.filter(created_on__lt = datetime.now() - timedelta(days=15)).delete()
