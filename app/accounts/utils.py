import environ
import logging
import pytz
from django.db.models import Q,F,Count,Sum,Min,Max
import os
from credentials.models import *
from accounts.models import *
from logger.models import *
from threading import Thread
from accounts.constants import *
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.core.mail import EmailMultiAlternatives,EmailMessage,get_connection
from pyfcm import FCMNotification
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from datetime import datetime,date,timedelta
from django.db.models import Q 
from rest_framework.authtoken.models import Token 
from twilio.rest import Client
from PIL import Image
from django.db.models import Exists,OuterRef,F
from django.db.models.functions import Radians, Power, Sin, Cos, ATan2, Sqrt, Radians
from typing import List,Iterable
from pathlib import Path
from django.contrib import messages
from django.http import HttpResponse,HttpRequest
from django.core.files.storage import FileSystemStorage
from weasyprint import HTML
from django.contrib.sites.models import Site
from rest_framework.exceptions import ValidationError
from rest_framework import status
from dateutil.relativedelta import relativedelta
from user_agents import parse
from subscription.models import *
from ecommerce.models import DiscountAd
import random
import string
from accounts.tasks import *
from wardrobe.models import *


db_logger = logging.getLogger('db')
env = environ.Env()
environ.Env.read_env()


def get_admin():
    '''
    Get Superuser 
    '''
    admin = User.objects.filter(is_superuser=True,role_id=ADMIN).last()
    return admin

def bulk_send_user_email(
        request:HttpRequest, user:User, template_name:str, mail_subject:str, to_email:str,
        token:str, description:str, title:str, password:str, temp:bool=True,addon_context={},attachments=[],assign_to_celery:bool=True
        ):
    '''
        Sends email to user
        `Uses Threading` to make this a background process.
        Args:
            request (HTTPRequest): `HTTPRequest` object
            user (User): Recipient `User`
            template_name (str): Template to render as a string
            mail_subject (str): Email subject
            to_email (str): Recepient email
            token (str): `User's` Token
            description (str): Email Description
            title (str): Email Title
            password (str): Password
            temp (bool): `False` if user is anonymous else `True` 
    '''
    if assign_to_celery:
        request = None ## for celery set request to None
        send_user_email.apply_async(args=(request,user,template_name,mail_subject,to_email,token,description,title,password,temp,addon_context,attachments)) 
    else:
        Thread(target=send_user_email,args=(request,user,template_name,mail_subject,to_email,token,description,title,password,temp,addon_context,attachments)).start()

def get_or_none(model_name, error_message, **kwargs):
    """
        Either return a single object or return validation error as a response.
    """
    try:
        return model_name.objects.get(**kwargs)
    except:
        raise ValidationError({"message": error_message, "status": status.HTTP_400_BAD_REQUEST})    

def get_pagination(request: HttpRequest, data: Iterable, **kwagrs):
    '''
        Dynamic Pagination if `required_page_size` is provided in **kwargs else uses Default PAGE SIZE
        Args:
            request (HTTPRequest): `HTTPRequest` object
            data (QuerySet):`QuerySet` object
    '''
    page_size = int(kwagrs['required_page_size']) if  'required_page_size' in kwagrs.keys() else PAGE_SIZE
    page = request.GET.get('page', 1)
    paginator = Paginator(data, page_size)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    except Exception as e:
        data = None 
    return data

def get_pagination1(request:HttpRequest,data:Iterable,number:int):
    '''
        Multiple pagination on same admin page 
        Args:
            request (HTTPRequest): `HTTPRequest` object
            data (QuerySet):`QuerySet` object
            number (int):`int` object representing unique queryset on the web page
    '''
    if not number:
        number=""
    page = request.GET.get(f'{number}page', 1)
    paginator = Paginator(data, PAGE_SIZE)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)
    except Exception as e:
        data = None 
    return data

def get_ip_address(request):
    '''
        Provides ip address from `request`
        Args:
            request (HTTPRequest): `HTTPRequest` object
    '''
    try:
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
        if ip_address:
            ip_address = ip_address.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')
    except Exception as e:
        db_logger.exception(e)
        ip_address=None
    return ip_address

def create_login_history(request:HttpRequest, user_email:str, mobile_no:str, status:int, country_code:str):
    '''
        Creates User Login History
        Args:
            request (HTTPRequest): `HTTPRequest` object
            user_email (str): user email
            mobile_no (str): user mobile number
            country_code (str): user country code
            status (int): 1:SUCCESS, 2:FAILURE
    '''
    site=Site.objects.first()
    if request.is_secure():
        protocol = 'https'
    else:
        protocol = 'http'
    if site: 
        url = f"{protocol}://{site.domain}{request.path}"
    else:
        url = f"{protocol}://"+request.META.get("REMOTE_ADDR")+request.path   
    user_agent = parse(request.META.get("HTTP_USER_AGENT"))
    LoginHistory.objects.create(
        user_ip = request.META.get("REMOTE_ADDR"),
        user_agent = str(user_agent.browser),
        status = status,
        url = url,
        user_email=user_email,
        mobile_no = mobile_no,
        country_code = country_code 
    )

def convert_to_utc(data:datetime, user_timezone:str):
    '''
        Converts Local datetime to UTC datetime.
        Args:
            data (datetime): `Datetime` object
            user_timezone (str): User Timezone
    '''
    local_tz = pytz.timezone(user_timezone if user_timezone else DEFAULT_TIMEZONE)
    UTC_tz = pytz.timezone("UTC")
    return datetime.strptime(str(UTC_tz.normalize(local_tz.localize(data).astimezone(UTC_tz))).split("+")[0], "%Y-%m-%d %H:%M:%S")

def user_authenticate(email:str, password:str):
    '''
        Authenticates User using his email/mobile_no and password
        Args:
            email (str): `str` object, accepts email and mobile number both
            country_code (str): `str` object, accepts country code in case of mobile number authentication else `None`
            password (str): `str` object, accepts password for the user authentication
    '''
    user = User.objects.filter(Q(email=email)|Q(username=email)|Q(mobile_no=email)).order_by('created_on').last()
    if user.check_password(password):
        return user
    else:
        return None

def convert_to_local_timezone(time_zone:str, date_time:str):
    '''
        Converts UTC time to Local Timezone.
        Args:
            time_zone (str): output `timezone`
            date_time (str): `UTC` Datetime string object
    '''
    try:
        local_tz = pytz.timezone("UTC")
        UTC_tz = pytz.timezone(time_zone)
        return datetime.strptime(str(UTC_tz.normalize(local_tz.localize(date_time).astimezone(UTC_tz))).split("+")[0], "%Y-%m-%d %H:%M:%S.%f")
    except Exception as e:
        db_logger.exception(e)
        return datetime.strptime(str(UTC_tz.normalize(local_tz.localize(date_time).astimezone(pytz.timezone('GMT')))).split("+")[0], "%Y-%m-%d %H:%M:%S")

def get_pages_data(page:int, data):
    '''
        Returns Pagination Data : Start, End, Meta Data
        Args:
            page (int): Page Number (starts from 1)
            data (QuerySet): `QuerySet` to apply pagination
    '''
    if page:
        if str(page) == '1':
            start = 0
            end = start + API_PAGINATION
        else:
            start = API_PAGINATION * (int(page)-1)
            end = start + API_PAGINATION
    else:
        start = 0
        end = start + API_PAGINATION
    page_data_value = Paginator(data, API_PAGINATION)	
    last_page = True if page_data_value.num_pages == int(page if page else 1) else False
    meta_data = { 
        "page_count": page_data_value.num_pages,
        "total_results": data.count(),
        "current_page_no": int(page if page else 1),
        "limit": API_PAGINATION,
        "last_page": last_page
    }
    return start,end,meta_data

def bulk_send_notification(
        created_by:User, created_for:List[User], title:str, description:str, notification_type:int, obj_id:str,assign_to_celery:bool=True
        ):
    '''
        Sends FCM and database notification to user
        `Uses Threading` to make this a background process.        
        Args:
            created_by (User): Created By `User` object
            created_for (`List[User]`): Recipient `User` objects List
            title (str): Notification Title
            description (str): Notification Description
            notification_type (int): Notification Type `int` object
            obj_id (str): object id to redirect
    '''
    if created_for:
        created_for = [str(i.id) for i in created_for]
    
    if assign_to_celery:
        send_notification.apply_async(args=(created_by,created_for,title,description,notification_type,obj_id))
    else:
        Thread(target=send_notification,args=(created_by,created_for,title,description,notification_type,obj_id)).start()

# def send_text_message(body:str, to_num:str):
#     '''
#         Send text message through twilio
#         Args:
#             body (str): Message Text
#             to_num (str): <Country Code><Mobile Number> (i.e. +919876543210)
#     '''
    
#     twilio_config = get_twilio_key()
#     account_sid = twilio_config.get('account_sid')
#     auth_token = twilio_config.get('auth_token')
#     from_num = twilio_config.get('from_num')
#     body = body
#     client = Client(account_sid, auth_token) 
#     try:
#         client.messages.create(from_= from_num, body=body, to = to_num)
#     except Exception as e:
#         db_logger.exception(e)
#     return body

def get_week_dates():
    '''
        Returns list of dates for current week
    '''
    today_date = date.today()
    weekday = today_date.isoweekday()
    start = today_date - timedelta(days=weekday)
    return [start + timedelta(days=d) for d in range(7)]

def query_filter_constructer(request,object_queryset,query_look_up):
    """
    For filter objects only on get method
    Args:
        request (HttpRequest): `HttpRequest` object
        object_queryset (QuerySet): `QuerySet` object
        query_look_up (dict): `dict` object for query lookups

        query_lookup dict format:

        {
            '<key= query_lookup>':'<value= lookup_value>'
        }
    """
    filter_params = {}
    for lookup in query_look_up.keys():
        lookup_value = request.GET.get(f'{query_look_up[lookup]}','').strip()
        if lookup_value:
            filter_params[lookup] = lookup_value

    if filter_params:
        return object_queryset.filter(**filter_params) 
    else:
        return object_queryset

def update_object(self,request, model, fields: list):
    model_object = model.objects.filter(id=self.kwargs['id'])
    data = {field: request.POST.get(field) for field in fields}
    if model.objects.filter(**data).exclude(id=self.kwargs['id']).exists():
        messages.error(request, 'Data already exists.')
        return False
    else:
        model_object.update(**data)
        messages.success(request, 'Data updated successfully!')
        return True

def activate_subscription(user,activate_purchased_plan:SubscriptionPlans=None):
    ## Warning : This function is also used on cronjob to renew plan
    if not activate_purchased_plan:
        upcomming_plan =  UserPlanPurchased.objects.filter(purchased_by=user,status = USER_PLAN_IN_QUEUE).order_by('created_on').first()
    else:
        upcomming_plan = activate_purchased_plan ## if specify which plan have to activate  
        
    ## check use have any active plan or not 
    if not UserPlanPurchased.objects.filter(purchased_by=user,status = USER_PLAN_IN_QUEUE).exists() and upcomming_plan:
        upcomming_plan.status = USER_PLAN_IN_QUEUE
        upcomming_plan.activated_on = datetime.now()
        ## set plan expiry
        if upcomming_plan.validity == MONTHLY_PLAN:
            expiry_date = datetime.now() + relativedelta(months=upcomming_plan.month_year)
        elif  upcomming_plan.validity == YEARLY_PLAN:
            expiry_date = datetime.now() + relativedelta(years=upcomming_plan.month_year)

        upcomming_plan.expire_on = expiry_date
        
        ## set user plan status 
        user.is_plan_purchased = True
        user.is_subscription_active = True
        user.plan_activated_on = datetime.now()
        user.plan_expire_on = expiry_date

        upcomming_plan.save()
        user.save()

def generate_plan_id():
    code = str(random.randint(1000000, 9999999))
    generated_id="SUB-"+code
    if UserPlanPurchased.objects.filter(plan_id = generated_id):
        generate_plan_id()
    else:
        return generated_id

def is_first_time_subscription_purchase(user:User):
    validated_data = {"is_valid":True,"message":""}
    already_purchased= UserPlanPurchased.objects.filter(purchased_by=user).exists()
    if already_purchased :
        validated_data['is_valid'] = False
        validated_data['message'] = "Invalid subscription purchase request"
    return validated_data

def render_to_pdf_file(request:HttpRequest,template_src:str, context:dict={},file_name:str="booking_invoice"):
    html_string = render_to_string(template_src, context)
    if request:
        base_url=request.build_absolute_uri()
    else:
        site=Site.objects.first()
        protocol="https://" if USE_HTTPS else "http://"
        base_url= f"{protocol}{site.domain}"
    html = HTML(string=html_string,base_url = base_url)
    html.write_pdf(target=f'/tmp/{file_name}.pdf',presentational_hints=True)
    fs = FileSystemStorage('/tmp')
    with fs.open(f'{file_name}.pdf') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{file_name}.pdf"'
            return response
    return None

def generate_discount_code(prefix="DIS", length=6, suffix=None):
    chars = string.ascii_uppercase + string.digits
    code_body = ''.join(random.choices(chars, k=length))
    code = f"{prefix}-{code_body}"
    if DiscountAd.objects.filter(discount_code = code):
        generate_discount_code()
    else:
        return code
    

    