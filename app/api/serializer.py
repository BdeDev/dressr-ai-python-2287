from static_pages.models import *
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework.authtoken.models import Token 
from contact_us.models import *
from api.helper import *

class UserSerializer(ModelSerializer):
    token = SerializerMethodField(read_only=True)
    profile_pic =SerializerMethodField()

    def get_profile_pic(self,obj):
        url=self.context.get('request').build_absolute_uri(obj.profile_pic.url) if obj.profile_pic else "" 
        if url:
            url=url.split('://')[1]
            return  'https://'+url if USE_HTTPS else 'http://' + url 
        return None
    
    def get_token(self, obj):
        token, _ = Token.objects.get_or_create(user=obj)
        return token.key

    class Meta:
        model=User
        fields= ("id","first_name","last_name","full_name","gender","role_id","last_login","profile_pic","email",
                 "mobile_no","country_code","country_iso_code","status","temp_otp","is_profile_setup","notification_enable","token",
                 "created_on","updated_on")


class MinorUserSerializer(ModelSerializer):
    profile_pic=SerializerMethodField()
    full_name=SerializerMethodField()

    def get_full_name(self,obj):
        if obj.role_id == ADMIN:
            return obj.username.capitalize()
        else:
            return obj.full_name

    def get_profile_pic(self,obj):
        url=self.context.get('request').build_absolute_uri(obj.profile_pic.url) if obj.profile_pic else "" 
        if url:
            url=url.split('://')[1]
            return  'https://'+url if USE_HTTPS else 'http://' + url 
        return None

    class Meta:
        model=User
        fields= ("id","full_name","profile_pic")


class PagesSerializer(ModelSerializer):
    class Meta:
        model = Pages
        fields = ('type_id','title','content')


class FaqSeializer(ModelSerializer):
    class Meta:
        model = FAQs
        fields = fields = ('id','question','answer','created_on')


class ContactUsSerializer(ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ('id','full_name','email','mobile_no','country_code','country_iso_code','location','link','message','created_on')


class NotificationSerializer(ModelSerializer):
    created_by=MinorUserSerializer()
    class Meta:
        model = Notifications
        fields = ("id", "title", "description", "is_read", "notification_type", "created_by", "created_for", "obj_id", "created_on")


class DeviceSerializer(ModelSerializer):
    user=MinorUserSerializer()

    class Meta:
        model = Device
        fields = ("id", "user", "device_type", "device_name", "device_token", "device_details", "created_on")

class SkinToneSerializer(ModelSerializer):

    class Meta:
        model = SkinTone
        fields = '__all__'

class HairColorSerializer(ModelSerializer):

    class Meta:
        model = HairColor
        fields = '__all__'