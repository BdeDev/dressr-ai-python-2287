import environ
import logging
import os
from credentials.models import *
from accounts.models import *
from logger.models import *
from accounts.constants import *
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from pathlib import Path
from django.http.request import HttpRequest
from django.core.mail import EmailMultiAlternatives
from typing import List,Literal,Type,Iterable
from pyfcm import FCMNotification
from django.contrib.sites.models import Site
from twilio.rest import Client
from accounts.celery_model_serializer import CustomModelTask
from .cron import *
from celery import shared_task

db_logger = logging.getLogger('db')
env = environ.Env()
environ.Env.read_env()

def get_fcm_key():
    '''
        Get fcm credentails data
    '''
    data={'fcm_file':'','project_id':''}
    BASE_DIR = Path(__file__).resolve().parent.parent
    fcm=FirebaseCredentials.objects.filter(active=True).last()
    if fcm:
        # data['fcm_file']=f'/app/media/{str(fcm.fcm_file)}' # on live
        data['fcm_file']=f'{BASE_DIR}/{str(fcm.fcm_file.url)}'
        data['project_id']=fcm.project_id
    else:
        fcm_json_path=os.path.join(BASE_DIR,'dressr-ai-e8352-firebase-adminsdk-1c3q9-268d531f5c.json')
        data['fcm_file']=fcm_json_path
        data['project_id']='dressr-ai-267d5'
    return data

@shared_task(base=CustomModelTask)
def send_push_notification(device_token,title,description,data_payload={}):
    try:
        fcm=get_fcm_key()
        push_service = FCMNotification(service_account_file=fcm['fcm_file'], project_id=fcm['project_id'])
        device_token = device_token
        push_service.notify(
            fcm_token=device_token,
            notification_title=title,
            notification_body=description,
            data_payload = data_payload,
            android_config = {
                "priority": "high",
                "notification": {
                    "title": f"{title}",
                    "body": f"{description}",
                    "notification_priority": "PRIORITY_HIGH",
                },
            }
        )
        return f'Success : Sent push notification'
    except Exception as e :
        # db_logger.exception(e)
        db_logger.exception("Exception: %s , Device token : %s. ", e, device_token)
        return f'Failed : Failed to sent push notification'
    return None

@shared_task(base=CustomModelTask)
def send_user_email(
    request: HttpRequest,
    user,
    template_name: str,
    mail_subject: str,
    to_email: str,
    token: str = "",
    description: str = "",
    title: str = "",
    password: str = "",
    temp: bool = False,
    addon_context: dict = None,
    attachments: list = None,
):
    """
    Send an email to a user with optional attachments and context.

    Args:
        request (HttpRequest): HTTP request object.
        user (User): Recipient user instance.
        template_name (str): Path to email template.
        mail_subject (str): Email subject line.
        to_email (str): Recipient email address.
        token (str): Token for user.
        description (str): Description for email content.
        title (str): Title for email content.
        password (str): Password to include in email.
        temp (bool): Flag to indicate anonymous user.
        addon_context (dict): Additional context for template rendering.
        attachments (list): List of file paths to attach.
    """

    try:
        # Determine current site info
        current_site = get_current_site(request) if request else Site.objects.first()
        protocol = "https" if getattr(settings, "USE_HTTPS", False) else "http"
        addon_context = addon_context or {}
        attachments = attachments or []
        context = {"domain": current_site.domain,"site_name": current_site.name,"protocol": protocol,"user": user,"email": to_email,"token": token,"description": description,"title": title,"subject": mail_subject,"password": password, **addon_context, }
        # Get sender email from SMTP settings or environment fallback
        smtp = SMTPSetting.objects.filter(is_active=True).first()
        from_email = smtp.from_email if smtp else settings.DEFAULT_FROM_EMAIL
        from_email_formatted = f"My Dressr <{from_email}>"

        # Render email content
        message = render_to_string(template_name, context)

        email_message = EmailMultiAlternatives(mail_subject, message, from_email_formatted, [to_email])
        email_message.attach_alternative(message, "text/html")

        # Attach files if any
        base_dir = Path(__file__).resolve().parent.parent
        for attachment in attachments:
            file_path = f"{base_dir}{attachment}"
            email_message.attach_file(str(file_path))

        # Log email before sending
        email_log = EmailLogger.objects.create(
            reciever=user if user else None,
            email_subject=mail_subject,
            email_template=message,
            recievers_email=to_email,
            sender_email=from_email,
            sent_status=EMAIL_PENDING,
        )
        # Send email and handle exceptions
        try:
            send_status = email_message.send()
        except Exception as exc:
            send_status = False
            db_logger.exception(f"Failed to send email: {exc}")

        # Update email log status
        email_log.sent_status = EMAIL_SENT if send_status else EMAIL_FAILED
        email_log.save()
        return f'Success : Sent Email ( {to_email} )'
    except Exception as exc:
        db_logger.exception(f"Exception in send_user_email: {exc}")
        return f'Failed : Exception in send_user_email: {exc}'

@shared_task(base=CustomModelTask)
def resend_email_function(email_log):
    ## function  will be use for resend email if email got failed
    smtp=SMTPSetting.objects.filter(is_active=True).first()
    from_email = smtp.email_host_user if smtp else settings.DEFAULT_FROM_EMAIL
    from_email_mail = f"My Dressr  <{from_email}>"  ## this formate is use to show : custom sender name along with email address to user email inbox

    recievers_emails = email_log.recievers_email.split(',')
    recievers_emails = [i.strip() for i in recievers_emails if i ]
    try :
        email_message = EmailMultiAlternatives(email_log.email_subject, None, from_email_mail, recievers_emails)
        html_email = email_log.email_template
        email_message.attach_alternative(html_email, 'text/html')
        status = email_message.send()
        email_log.sent_status = EMAIL_SENT
        email_log.save()  
        return f'Success : Sent Email ( {recievers_emails} )'
    except Exception as e:
        db_logger.exception(e)
        email_log.sent_status = EMAIL_FAILED
        email_log.save()  
        return f'Failed : Failed To Sent Email ( {recievers_emails} )'

@shared_task(base=CustomModelTask)
def send_email_with_template_html(user,email_subject,to_email,email_template_html):
    """
    This function will be use to send email , with complete html data only
    """
    try:
        # Get sender email from SMTP settings or environment fallback
        smtp = SMTPSetting.objects.filter(is_active=True).first()
        from_email = smtp.from_email if smtp else settings.DEFAULT_FROM_EMAIL
        from_email_formatted = f"Dreassr AI <{from_email}>"

        # Render email content
        html_email = email_template_html

        email_message = EmailMultiAlternatives(email_subject, html_email, from_email_formatted,[to_email])
        email_message.attach_alternative(html_email, "text/html")

        # Log email before sending
        email_log = EmailLogger.objects.create(
            reciever=user if user else None,
            email_subject=email_subject,
            email_template=html_email,
            recievers_email=to_email,
            sender_email=from_email,
            sent_status=EMAIL_PENDING,
        )
        # Send email and handle exceptions
        try:
            send_status = email_message.send()
        except Exception as exc:
            send_status = False
            db_logger.exception(f"Failed to send email: {exc}")

        # Update email log status
        email_log.sent_status = EMAIL_SENT if send_status else EMAIL_FAILED
        email_log.save()
        return f'Success : Sent Email ( {to_email} )'
    except Exception as exc:
        db_logger.exception(f"Exception in send_email_with_template_html: {exc}")
        return f'Failed : Exception in send_email_with_template_html: {exc}'

@shared_task(base=CustomModelTask)
def send_notification(
        created_by:User, created_for:List[User], title:str, description:str, notification_type:int, obj_id:str
        ):
    '''
        Sends FCM and database notification to user
        Args:
            created_by (User): Created By `User` object
            created_for (`List[User]`): Recipient `User` objects List
            title (str): Notification Title
            description (str): Notification Description
            notification_type (int): Notification Type `int` object
            obj_id (str): object id to redirect 
    '''
    if not created_by:
        created_by = User.objects.filter(is_superuser=True,role_id=ADMIN).last() 
    
    if created_for:
        created_for = User.objects.filter(id__in=created_for).order_by('-created_on')
    else:
        created_for = User.objects.filter(is_superuser=True,role_id=ADMIN)
        
    for user in created_for:
        try:
            if user.notification_enable:
                notification = Notifications.objects.create(
                    title = title,
                    description = description,
                    created_for = user,
                    obj_id = obj_id,
                    notification_type = notification_type,
                    created_by = created_by,
                )
                ## Send Push Notification
                device = Device.objects.filter(user=user).order_by('-created_on').first()
                if device:
                    if device.device_token:
                        data_payload = {
                            "title":title,
                            "description":description,
                            "notification_id":str(notification.id),
                            "obj_id":str(notification.obj_id),
                            "sender_id":str(notification.created_by.id) if notification.created_by else None,
                            "notification_type":str(notification_type if notification_type else 0),
                        }
                        send_push_notification(
                            device_token = device.device_token,
                            title = title,
                            description = description,
                            data_payload = data_payload
                        )       
        except Exception as exception:
            db_logger.exception(exception)
    return None

@shared_task(base=CustomModelTask)
def send_email_campaign_emails(campaign_template,user_emails_list):
    ## Send Email 
    smtp=SMTPSetting.objects.filter(is_active=True).first()
    from_email = smtp.email_host_user if smtp else settings.DEFAULT_FROM_EMAIL
    ## create log for email 
    email_subject = campaign_template.subject
    html_email = campaign_template.description
    
    email_to_log = ' , '.join(user_emails_list)
    email_log = EmailLogger.objects.create(
        reciever =  None,
        email_subject = email_subject,
        email_template = html_email,
        recievers_email = email_to_log, ## list of all emails
        sender_email = from_email,
        sent_status = EMAIL_PENDING
    )
    try :
        from_email_mail = f"Dreassr AI  <{from_email}>"  ## this formate is use to show : custom sender name along with email address to user email inbox
        email_message = EmailMultiAlternatives(email_subject, None, from_email_mail, user_emails_list )
        email_message.attach_alternative(html_email, 'text/html')
        status = email_message.send()
        email_log.sent_status = EMAIL_SENT
    except Exception as e:
        email_log.sent_status = EMAIL_FAILED
        db_logger.exception(e)
    email_log.save()  

    return None


# def get_twilio_key():
#     '''
#         Get twilio credentails data
#     '''
#     twilio=TwilioSetting.objects.filter(is_active=True).last()
#     data={
#         'account_sid':env('ACCOUNT_SID'),
#         'from_num':env('AUTH_TOKEN'),
#         'auth_token':env('AUTH_TOKEN')
#         }
#     if twilio:
#         data['account_sid']= twilio.account_sid
#         data['from_num'] = twilio.number
#         data['auth_token'] = twilio.token
#     return data



# def send_campaign_sms(campaign_template,user_list):
    # title = campaign_template.subject
    # html_description = campaign_template.description
    
    # body = f"{title}\n\n{html_description}"

    # twilio_config = get_twilio_key()
    # account_sid = twilio_config.get('account_sid')
    # auth_token = twilio_config.get('auth_token')
    # from_num = twilio_config.get('from_num')

    # client = Client(account_sid, auth_token) 
    # results = []
    # for to_num in user_list:
    #     try:
    #         message = client.messages.create(from_=from_num, body=body, to=to_num)
    #         results.append({"number": to_num, "status": "success", "sid": message.sid})
    #     except Exception as e:
    #         db_logger.exception(e)
    #         results.append({"number": to_num, "status": "failed", "error": str(e)})
    
    # return results