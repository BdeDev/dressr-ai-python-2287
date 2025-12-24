from accounts.common_imports import *
from django_db_logger .models import StatusLog
from .serializer import *
from .models import *
from accounts.utils import *
from accounts.tasks import *


"""
Error Logs Management 
"""
class ErrorLogsList(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        error_logs = StatusLog.objects.all().order_by('-create_datetime').only('id')
        error_logs = query_filter_constructer(request,error_logs,
            {
                "msg__icontains":"message",
                "trace__icontains":"message",
                "create_datetime__date":"created_on",
            }
        )
        return render(request, 'logger/error-logs-list.html',{
            "head_title":"Website Error Logs Management",
            "error_logs":get_pagination(request,error_logs),
            "message":request.GET.get('message',""),
            "trace":request.GET.get('trace',""),
            "created_on":request.GET.get('created_on',""),
            "total_objects":error_logs.count()
        })


class DeleteAllLogs(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        StatusLog.objects.all().delete()
        messages.success(request,"Error logs deleted Successfully!")
        return redirect('logger:error_logs_list')


class DeleteErrorLog(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        StatusLog.objects.get(id=self.kwargs['id']).delete()
        messages.success(request,"Error log deleted successfully!")
        return redirect('logger:error_logs_list')


class ViewErrorLog(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        error_log = StatusLog.objects.get(id=self.kwargs['id'])
        return render(request, 'logger/view-error-log.html',{"head_title":"Website Error Logs Management","error_log":error_log})


"""
Email Logs Management
"""
class EmailLogsList(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        email_logs = EmailLogger.objects.all().order_by('-created_on').only('id')
        email_logs = query_filter_constructer(request,email_logs,
            {
                "recievers_email__icontains":"recievers_email",
                "sender_email__icontains":"sender_email",
                "email_subject__icontains":"email_subject",
                "sent_status":"sent_status",
                "created_on__date":"created_on",
            }
        )
        if request.GET and not email_logs:
            messages.error(request, 'No Data Found')
        return render(request, 'email-logger/email-logs-list.html',{
            "head_title":"Email Logs Management",
            "email_logs":get_pagination(request,email_logs),
            "recievers_email":request.GET.get('recievers_email','') ,
            "sender_email":request.GET.get('sender_email',''),
            "email_subject":request.GET.get('email_subject',''),
            "sent_status":request.GET.get('sent_status',''),
            "created_on":request.GET.get('created_on',''),
            "total_objects":email_logs.count()
        })
    

class ViewEmailLog(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        email_log = EmailLogger.objects.get(id=self.kwargs['id'])
        return render(request, 'email-logger/view-email-log.html',{
            "head_title":"Email Logs Management",
            "email_log":email_log
        })


class DeleteEmailLogs(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        if EmailLogger.objects.all().exists():
            EmailLogger.objects.all().delete()
            messages.success(request,"Email logs deleted successfully!")
        else:
            messages.error(request,"No Email Logs Found!")
        return redirect('logger:email_logs_list')


class DeleteEmailLog(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        EmailLogger.objects.get(id=self.kwargs['id']).delete()
        messages.success(request, 'Email log deleted successfully!')
        return redirect('logger:email_logs_list')

## Resend Failed Email
class ResendEmail(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        email_log = EmailLogger.objects.get(id=self.kwargs['id'])
        email_log.sent_status = EMAIL_PENDING
        email_log.save()
        ## function to resend 
        Thread(target=resend_email_function, args=(email_log,)).start()
        messages.success(request, 'Process to sending email initiated successfully')
        return redirect('logger:view_email_log',id=email_log.id)

## Send Single Cutom Email

class SendCustomEmail(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=self.kwargs['id'])
        return render(request,'email-logger/send-email-to-user.html',{
            "head_title":'Email Logs Management',
            'user':user,
        })
    @method_decorator(admin_only)
    def post(self, request, *args, **kwargs):
        user = User.objects.get(id=self.kwargs['id'])
        to_email = user.email
        subject = request.POST.get('title').strip()
        description = request.POST.get('content').strip()
        full_name = request.POST.get('full_name').strip()
        # send email
        # send_email_with_template_html.apply_async(args=(user,subject,to_email,description))
        # bulk_send_user_email(
        #     request = request,
        #     user = None,
        #     template_name = "EmailTemplates/notification-email.html",
        #     mail_subject = subject,
        #     to_email = to_email,
        #     token = full_name,
        #     description =description,
        #     title = subject,
        #     password = "",
        #     assign_to_celery=True
        #     )
        messages.success(request,'Email sending process initiated successfully')
        return redirect('logger:email_logs_list')
    
    
class CrashLogs(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        logs = ApplicationCrashLogs.objects.all().order_by('-created_on')
        logs = query_filter_constructer(request,logs,
            {
                "error__icontains":"error",
                "link__icontains":"link",
                "referer_link__icontains":"referrer_link",
                "user_ip__icontains":"user_ip",
                "created_on__date":"created_on",
            }
        )
        if request.GET and not logs:
            messages.error(request, 'No Data Found')
        return render(request, 'application-logger/application-logs-list.html',{
            "head_title":"Application Error Logs Management",
            "logs":get_pagination(request,logs),
            "error":request.GET.get('error',""),
            "link":request.GET.get('link',""),
            "referrer_link":request.GET.get('referrer_link',""),
            "user_ip":request.GET.get('user_ip',""),
            "created_on":request.GET.get('created_on',""),
            "total_objects":logs.count()
        })


class ViewCrashLog(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        log = ApplicationCrashLogs.objects.get(id=self.kwargs['id'])
        return render(request, 'application-logger/view-application-log.html',{
            "head_title":"Application Error Logs Management",
            "log":log
        })


class DeleteAllCrashLogs(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        if ApplicationCrashLogs.objects.all().exists():
            ApplicationCrashLogs.objects.all().delete()
            messages.success(request,"Logs deleted successfully!")
        else:
            messages.error(request,"No error logs Found!")
        return redirect('logger:crash_logs')


class DeleteCrashLog(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        ApplicationCrashLogs.objects.get(id=self.kwargs['id']).delete()
        messages.success(request, 'Log deleted successfully!')
        return redirect('logger:crash_logs')


"""
Application Crash Log Management
"""

class CreateCrashLog(APIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = [MultiPartParser,FormParser]
    @swagger_auto_schema(
        operation_description="Create application crash log",
        manual_parameters=[
            openapi.Parameter('error', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('link', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('referer_link', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('user_ip', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('description', openapi.IN_FORM, type=openapi.TYPE_STRING),
        ],
        tags=['Application Crash log'],
        operation_id="Create application crash log",
    )
    def post(self, request, *args, **kwargs):
        try:
            ApplicationCrashLogs.objects.create(
                error = request.data.get('error'),
                link = request.data.get('link'),
                referer_link = request.data.get('referer_link'),
                user_ip = request.data.get('user_ip'),
                description = request.data.get('description')
            )
        except Exception as e:
            db_logger.exception(e)
        return Response({"message":"Crash Log Created Successfully!","status":status.HTTP_200_OK}, status=status.HTTP_200_OK)


class GetCrashLog(APIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = [MultiPartParser,FormParser]
    @swagger_auto_schema(
        operation_description="Get application crash log",
        tags=['Application Crash log'],
        operation_id="Get application crash log",
    )
    def get(self, request, *args, **kwargs):
        try:
            log=ApplicationCrashLogs.objects.all().order_by('-created_on').first()
        except Exception as e:
            db_logger.exception(e)
            return Response({"message":"Crash Log not found!","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        if log:
            data=ApplicationCrashLogsSerializer(log,context={"request":request}).data
            return Response({"data":data,"status":status.HTTP_200_OK}, status=status.HTTP_200_OK)
        else:
            return Response({"data":[],"status":status.HTTP_200_OK}, status=status.HTTP_200_OK)

"""
Email campaigns
"""
class CampaignTemplateList(View):
    """
        Mail Drafts List
    """
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        campaigns_templates=EmailDraftTemplates.objects.all().order_by('-created_on')
        campaigns_templates = query_filter_constructer(request,campaigns_templates,
            {
                "subject__icontains":"subject",
                "created_on__date":"created_on"
            }
        )
        if request.GET and not campaigns_templates:
            messages.error(request, 'No Data Found')
        return render(request, 'email-campaigns/campaign-template-list.html', {
            'head_title': 'Email Campaigns Management',
            'campaigns_templates':get_pagination(request,campaigns_templates),
            "search_filters":request.GET.copy(),
            "total_objects":campaigns_templates.count()
        })

class SaveCampaignTemplate(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        draft=None
        if request.GET.get('draft_id'):
            draft=EmailDraftTemplates.objects.get(id=request.GET.get('draft_id'))
        current_site = get_current_site(request)
        return render(request, 'email-campaigns/add-campaign-template.html', {
            'head_title': 'Email Campaigns Management',
            'domain':current_site.domain,
            'protocol': 'https' if USE_HTTPS else 'http',
            'draft':draft
        })

    """
        Save Mail Draft
    """
    @method_decorator(admin_only)
    def post(self, request, *args, **kwargs):
        subject = request.POST.get('title').strip()
        description = request.POST.get('content').strip()
        if request.GET.get('draft_id'):
            draft=EmailDraftTemplates.objects.get(id=request.GET.get('draft_id'))
            draft.subject=subject
            draft.description=description
            draft.save()
        else:
            EmailDraftTemplates.objects.create(
                subject=subject,
                description=description
            )
        messages.success(request,'Campaigns template saved successfully.')
        return redirect("logger:campaign_templates")


class DeleteCampaignTemplate(View):
    """
        Delete Mail Draft
    """
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        draft=EmailDraftTemplates.objects.get(id=self.kwargs.get('id'))
        draft.delete()
        messages.success(request,"Draft deleted successfully!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



class SendCampaignEmails(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        campaign_template = EmailDraftTemplates.objects.get(id=self.kwargs.get('id'))
        users = User.objects.all()
        user_count_data = {
            "active_users":users.filter(status=ACTIVE).count(),
            "inactive_users":users.filter(status=INACTIVE).count(),
            "deleted_users":users.filter(status=DELETED).count(),
        }
        return render(request, 'email-campaigns/send-campaign-email.html', {
            'head_title': 'Email Campaigns Management',
            "campaign_template":campaign_template,
            "user_count_data":user_count_data,
        })
    @method_decorator(admin_only)
    def post(self, request, *args, **kwargs):
        campaign_template = EmailDraftTemplates.objects.get(id=self.kwargs.get('id'))
        all_on_emails = [i.strip() for i in request.POST.getlist('addon_email') if request.POST.getlist('addon_email')]
        user_status = []
        if request.POST.getlist('active_users'):
            user_status.append(ACTIVE)
        if request.POST.getlist('inactive_users'):
            user_status.append(INACTIVE)
        if request.POST.getlist('deleted_users'):
            user_status.append(DELETED)

        if user_status:
            users = User.objects.filter(status__in = user_status).values_list('email',flat=True)
            all_on_emails.extend(users)

        Thread(target=send_email_campaign_emails,args=(campaign_template,all_on_emails)).start()
        messages.success(request,'Email sending process initiated successfully')
        return redirect('logger:send_campaign_email',id=campaign_template.id)
    

"""
SMS campaigns
"""
class SMSCampaignTemplateList(View):
    """
        SMS Drafts List
    """
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        campaigns_templates=SMSDraftTemplates.objects.all().order_by('-created_on')
        campaigns_templates = query_filter_constructer(request,campaigns_templates,
            {
                "subject__icontains":"subject",
                "created_on__date":"created_on"
            }
        )
        if request.GET and not campaigns_templates:
            messages.error(request, 'No Data Found')
        return render(request, 'sms-campaigns/campaign-template-list.html', {
            'head_title': 'SMS Campaigns Management',
            'campaigns_templates':get_pagination(request,campaigns_templates),
            "search_filters":request.GET.copy(),
            "total_objects":campaigns_templates.count()
        })

class SaveSMSCampaignTemplate(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        draft=None
        if request.GET.get('draft_id'):
            draft=SMSDraftTemplates.objects.get(id=request.GET.get('draft_id'))
        return render(request, 'sms-campaigns/add-campaign-template.html', {
            'head_title': 'SMS Campaigns Management',
            'draft':draft
        })

    """
        Save Mail Draft
    """
    @method_decorator(admin_only)
    def post(self, request, *args, **kwargs):
        subject = request.POST.get('title').strip()
        description = request.POST.get('content').strip()
        if request.GET.get('draft_id'):
            draft=SMSDraftTemplates.objects.get(id=request.GET.get('draft_id'))
            draft.subject=subject
            draft.description=description
            draft.save()
        else:
            SMSDraftTemplates.objects.create(
                subject=subject,
                description=description
            )
        messages.success(request,'Campaigns template saved successfully.')
        return redirect("logger:sms_campaign_templates")


class DeleteSMSCampaignTemplate(View):
    """
        Delete Mail Draft
    """
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        draft=SMSDraftTemplates.objects.get(id=self.kwargs.get('id'))
        draft.delete()
        messages.success(request,"Draft deleted successfully!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



class SendCampaignSMS(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        campaign_template = SMSDraftTemplates.objects.get(id=self.kwargs.get('id'))
        users = User.objects.all()
        user_count_data = {
            "active_users":users.filter(status=ACTIVE).count(),
            "inactive_users":users.filter(status=INACTIVE).count(),
            "deleted_users":users.filter(status=DELETED).count(),
        }
        return render(request, 'sms-campaigns/send-campaign-email.html', {
            'head_title': 'SMS Campaigns Management',
            "campaign_template":campaign_template,
            "user_count_data":user_count_data,
        })
    @method_decorator(admin_only)
    def post(self, request, *args, **kwargs):
        campaign_template = SMSDraftTemplates.objects.get(id=self.kwargs.get('id'))
        
        all_mobile_numbers = []
        addon_country_code = request.POST.getlist('country_code')
        addon_mobile_no = request.POST.getlist('addon_mobile_no')
        if addon_mobile_no and addon_country_code:
            combine_data = zip(addon_country_code,addon_mobile_no)
            all_mobile_numbers = [f'{i.strip()}{j.strip()}' for i, j in combine_data]

        user_status = []
        if request.POST.getlist('active_users'):
            user_status.append(ACTIVE)
        if request.POST.getlist('inactive_users'):
            user_status.append(INACTIVE)
        if request.POST.getlist('deleted_users'):
            user_status.append(DELETED)

        if user_status:
            users_mobile_numbers = User.objects.filter(status__in = user_status).annotate(full_mobile=Concat('country_code', 'mobile_no')).values_list('full_mobile',flat=True)
            all_mobile_numbers.extend(users_mobile_numbers)

        # Thread(target=send_campaign_sms,args=(campaign_template,all_mobile_numbers)).start()
        messages.success(request,'SMS sending process initiated successfully')
        return redirect('logger:send_campaign_sms',id=campaign_template.id)
    
