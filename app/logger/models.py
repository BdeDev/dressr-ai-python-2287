from accounts.models import *
from accounts.models import *


class EmailLogger(CommonInfo):
    reciever = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    email_template = models.TextField(null=True, blank=True)
    email_subject = models.TextField(null=True, blank=True)
    recievers_email = models.TextField(null=True, blank=True) ## with be commaa seprated emails on email campaign
    sender_email = models.CharField(null=True, blank=True, max_length=100)
    sent_status = models.PositiveIntegerField(default=EMAIL_PENDING,choices=EMAIL_STATUS,null=True, blank=True)
    class Meta:
        db_table = 'email_logger'
       

class ApplicationCrashLogs(CommonInfo):
    error = models.TextField(null=True, blank=True)
    link = models.TextField(null=True, blank=True)
    referer_link = models.TextField(null=True, blank=True)
    user_ip = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'application_crash_logs'


class EmailDraftTemplates(CommonInfo):
    subject = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'email_draft_templates'
       

class SMSDraftTemplates(CommonInfo):
    subject = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'sms_draft_templates'
        