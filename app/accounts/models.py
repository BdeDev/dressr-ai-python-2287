import uuid
from .constants import *
from django.db import models
from django.contrib.auth.models import AbstractUser,Permission
import environ

env = environ.Env()
environ.Env.read_env()

class CommonInfo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_on = models.DateTimeField(auto_now=True,null=True,blank=True)

    class Meta:
        abstract = True

class Image(CommonInfo):
    image = models.ImageField(upload_to='images/',null=True,blank=True)
    class Meta:
        managed = True
        db_table = 'images'

class User(AbstractUser,CommonInfo):
    username = models.CharField(max_length=255,blank=True, null=True, unique=True)
    first_name = models.CharField(max_length=50, null=True,blank=True)
    last_name = models.CharField(max_length=50, null=True,blank=True)
    full_name = models.CharField(max_length=50, null=True,blank=True)
    mobile_no = models.CharField(max_length=20, null=True, blank=True)
    dob = models.CharField(max_length=20, null=True, blank=True)
    temp_otp = models.CharField(max_length=10, null=True, blank=True)
    country_iso_code = models.CharField(max_length=10, null=True, blank=True)
    country_code = models.CharField(max_length=20, null=True, blank=True)
    profile_pic = models.FileField(upload_to='profile_pic/', blank=True, null=True)
    user_image = models.FileField(upload_to='user_image/', blank=True, null=True)
    role_id = models.PositiveIntegerField(default=ADMIN,choices=USER_ROLE,null=True, blank=True)
    status = models.PositiveIntegerField(default=ACTIVE, choices=USER_STATUS,null=True, blank=True)
    gender = models.PositiveIntegerField(choices=GENDER, null=True, blank=True)
    is_profile_setup = models.BooleanField(default=False)
    notification_enable = models.BooleanField(default=True)
    email_notification = models.BooleanField(default=False)
    sms_notification = models.BooleanField(default=False)
    body_type = models.ForeignKey('BodyType',on_delete=models.SET_NULL,null=True,blank=True)
    hieght_cm = models.FloatField(default=0.0, null=True, blank=True)
    skin_tone = models.ForeignKey('SkinTone', on_delete=models.SET_NULL,null=True,blank=True)
    hair_color = models.ForeignKey('HairColor', on_delete=models.SET_NULL,null=True,blank=True)
    others = models.TextField(null=True,blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)

    refered_by = models.ForeignKey('accounts.User',on_delete=models.CASCADE,null=True,blank=True)
    referral_code = models.CharField(max_length=20,null=True,blank=True)
    ## Address attributes
    address = models.CharField(max_length=255,blank=True, null=True)
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    
    ## subscription 
    is_plan_purchased = models.BooleanField(default=False)
    is_subscription_active = models.BooleanField(default=False)
    plan_activated_on = models.DateTimeField(auto_now=False,null=True,blank=True)
    plan_expire_on = models.DateTimeField(auto_now=False,null=True,blank=True)
    
    class Meta:
        db_table = 'user'

    def __str__(self):
        return str(self.first_name)

class SkinTone(CommonInfo):
    title = models.CharField(max_length=50, null=True,blank=True)
    color_code = models.CharField(max_length=20, null=True,blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'skin_tone'

class HairColor(CommonInfo):
    title = models.CharField(max_length=50, null=True,blank=True)
    color_code = models.CharField(max_length=20, null=True,blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'hair_color'

class BodyType(CommonInfo):
    title = models.CharField(max_length=50, null=True,blank=True)
    icon = models.ImageField(upload_to='body_icons/',blank=True,null=True)
    description = models.TextField(null=True,blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'body_type'

class Profile(CommonInfo):
    user = models.OneToOneField(User, on_delete=models.CASCADE,blank=True, null=True)
    profile_name = models.CharField(max_length=50, null=True,blank=True)
    avatar_url = models.URLField(blank=True, null=True)

    class Meta:
        db_table = 'user_profile'

class Device(CommonInfo):
    user = models.ForeignKey('User',null=True,blank=True,on_delete=models.CASCADE)
    device_type = models.PositiveIntegerField(choices=DEVICE_TYPE,null=True,blank=True)
    device_name = models.CharField(max_length=255,null=True,blank=True)
    device_token = models.TextField(null=True,blank=True)

    class Meta:
        db_table = 'device'

class LoginHistory(CommonInfo):
    user_ip = models.CharField(max_length=255, null=True, blank=True)
    user_agent = models.CharField(max_length=255, null=True, blank=True)
    status = models.PositiveIntegerField(null=True, blank=True, choices=LOGIN_STATE)
    url = models.CharField(max_length=255, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    user_email = models.CharField( max_length=255, null=True, blank=True)
    mobile_no = models.CharField(max_length=20, null=True, blank=True)
    country_code = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = 'login_history'

class Notifications(CommonInfo):
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    notification_type = models.PositiveIntegerField(null=True, blank=True, choices=NOTIFICATION_TYPE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications", null=True, blank=True)
    created_for = models.ForeignKey(User, on_delete=models.CASCADE, related_name="_notifications", null=True, blank=True)
    obj_id =models.CharField(max_length=255,null=True,blank=True)

    class Meta:
        db_table = 'notifications'

class Banners(CommonInfo):
    title = models.CharField(max_length=255,blank=True,null=True)
    image = models.ImageField(upload_to='banner',blank=True,null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'banners'