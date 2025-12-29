from django.db import models
from accounts.models import *

class SMTPSetting(CommonInfo):
    email_backend = models.TextField(null=True, blank=True)
    email_host = models.TextField(null=True, blank=True)
    email_port = models.CharField(max_length=255, blank=True, null=True)
    use_tls = models.BooleanField(default=True, blank=True, null=True)
    email_host_user = models.CharField(max_length=255, blank=True, null=True)
    from_email = models.CharField(max_length=255, blank=True, null=True)
    email_host_password = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=False, blank=True, null=True)

    class Meta:
        db_table = 'smtp_settings'

class FirebaseCredentials(CommonInfo):
    fcm_file = models.FileField(upload_to="fcm_file",null=True,blank=True)
    project_id = models.CharField(max_length=100,null=True,blank=True)
    active = models.BooleanField(default=False)

    class Meta:
        db_table = 'firebase_credentials'
       
class StripeSetting(CommonInfo):
    test_secretkey = models.CharField(max_length=100,null=True,blank=True)
    test_publishkey = models.CharField(max_length=100,null=True,blank=True)
    active = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'stripe_setting'
        

class TwilioSetting(CommonInfo):
    account_sid = models.TextField(null=True, blank=True)
    number = models.TextField(null=True, blank=True)
    token = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=False, blank=True, null=True)

    class Meta:
        db_table = 'twilio_settings'
       

class LightXEditorCredentials(CommonInfo):
    api_key = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=False, blank=True, null=True)

    class Meta:
        db_table = 'lightx_editor'