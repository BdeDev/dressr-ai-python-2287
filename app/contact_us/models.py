from django.db import models
from accounts.models import *

class ContactUs(CommonInfo):
    full_name = models.CharField(max_length=255, null=True, blank=True)
    subject = models.CharField(max_length=255,null=True,blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    mobile_no = models.CharField(max_length=20, null=True, blank=True)
    country_code = models.CharField(max_length=10, null=True, blank=True)
    country_iso_code = models.CharField(max_length=10, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    is_replied = models.BooleanField(default=False)

    class Meta:
        db_table = 'contactus'

class ContactUsReply(CommonInfo):
    contact = models.ForeignKey('ContactUs',null=True,blank=True,on_delete=models.CASCADE)
    reply_message = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name="replied_to")

    class Meta:
        db_table = 'contactus_reply'

class SocialLinks(CommonInfo):
    instagram = models.TextField(null=True, blank=True)
    twitter = models.TextField(null=True, blank=True)
    facebook=models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    class Meta:
        db_table = 'social_links'
        