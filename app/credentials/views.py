from accounts.utils import get_pagination
from .models import *
from accounts.common_imports import *
from django.http import HttpResponseRedirect

"""
SMTP keys Management
"""
@method_decorator(admin_only,name='dispatch')
class SMTPPrompt(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'email-logger/send-custom-email.html', {
            'head_title': 'SMTP Management',
        })

    def post(self, request, *args, **kwargs):
        to_email = request.POST.get('to_email').strip()
        subject = request.POST.get('title').strip()
        description = request.POST.get('content').strip()
        full_name = request.POST.get('full_name').strip()
        # send email
        bulk_send_user_email(
            request = request,
            user = None,
            template_name = "EmailTemplates/notification-email.html",
            mail_subject = subject,
            to_email = to_email,
            token = full_name,
            description =description,
            title = subject,
            password = "",
            assign_to_celery=False
            )
        messages.success(request,'Email sending process initiated successfully')
        return redirect('credentials:smtp_prompt')


class SMTPListView(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        smtp_settings = SMTPSetting.objects.all().order_by('-created_on').only('id')
        smtp_settings = query_filter_constructer(
            request, smtp_settings,
            {
                "email_host__icontains": "email_host",
                "email_port__icontains": "email_port",
                "email_host_user__icontains": "email_host_user",
                "use_tls": "use_tls",
                "is_active": "is_active",
                "created_on__date": "created_on",
            })

        if not smtp_settings and request.GET:
            messages.error(request, 'No Data Found')
        return render(request, 'credentials/smtp_settings/smtp-list.html',{
            "head_title":"SMTP Management",
            "smtp_settings": get_pagination(request, smtp_settings),
            "total_objects": smtp_settings.count(),
        })

class ViewSMTP(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        smtp = SMTPSetting.objects.get(id=self.kwargs['id'])
        return render(request, 'credentials/smtp_settings/view-smtp.html',{"smtp":smtp,"head_title":"SMTP Management"})


class AddSMTPView(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        return render(request, 'credentials/smtp_settings/add-smtp.html',{"head_title":"SMTP Management"})
    @method_decorator(admin_only)
    def post(self, request, *args, **kwargs):
        response=CustomRequiredFieldsValidator.validate_web_field(self,request,
            [
                {"field_name": "email_host", "method": "post", "error_message": "please enter email host"},
                {"field_name": "email_port", "method": "post", "error_message": "please enter email port"},
                {"field_name": "email_host_user", "method": "post", "error_message": "please enter email host user"},
                {"field_name": "from_email", "method": "post", "error_message": "please enter from email"},
                {"field_name": "email_host_password", "method": "post", "error_message": "please enter email host password"},
            ]
        )
        if not response:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        email_backend = "django.core.mail.backends.smtp.EmailBackend"
        smtp_fields = ['email_host', 'email_port', 'email_host_user','use_tls', 'email_host_password','from_email']
        smtp_data = {field: request.POST.get(field).strip() for field in smtp_fields}
        if SMTPSetting.objects.filter(email_backend=email_backend, **smtp_data).exists():
            messages.error(request, 'Credentials already exist with this data')
            return redirect('credentials:add_smtp')
        smtp_detail = SMTPSetting.objects.create(email_backend=email_backend,**smtp_data)
        smtp_detail.save()
        messages.success(request, 'Key added successfully!')
        return redirect('credentials:view_smtp',id=smtp_detail.id)


class EditSMTP(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        smtp = SMTPSetting.objects.get(id=self.kwargs['id'])
        return render(request, 'credentials/smtp_settings/edit-smtp.html',{"head_title":"SMTP Management","smtp":smtp})
    @method_decorator(admin_only)
    def post(self, request, *args, **kwargs):
        fields = ['email_host', 'email_port', 'email_host_user','use_tls','email_host_password','from_email']        
        update_object(self,request,SMTPSetting,fields)
        return redirect('credentials:view_smtp',id=self.kwargs['id'])

class DeleteSMTP(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        SMTPSetting.objects.get(id=self.kwargs['id']).delete()
        messages.success(request, 'Key Deleted Successfully!')
        return redirect('credentials:smtp_list')

class ActivateDeActiveSMTP(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        page = SMTPSetting.objects.get(id=self.kwargs['id'])
        if page.is_active:
            page.is_active=False
            messages.success(request,'Key deactivated Successfully!')
        else:
            SMTPSetting.objects.all().update(is_active = False)
            page.is_active = True   
            messages.success(request,'Key activated Successfully!')
        page.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    

'''
Firebase 
'''
class FirebaseKeysList(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        firebase_credentials = FirebaseCredentials.objects.all().order_by('-created_on').only('id')
        firebase_credentials = query_filter_constructer(
            request, firebase_credentials,
            {
                "project_id__icontains": "project_id",
                "active": "active",
                "created_on__date": "created_on",
            })

        if not firebase_credentials and request.GET:
            messages.error(request, 'No Data Found')
        return render (request,'credentials/firebase/credentials-list.html',{
            'firebase_credentials':get_pagination(request,firebase_credentials),
            'head_title':'Firebase Management',
            "total_objects": firebase_credentials.count(),
        })
    
    @method_decorator(admin_only)
    def post(self,request,*args,**kwargs):
        if FirebaseCredentials.objects.filter(project_id=request.POST.get('project_id')):
            messages.error(request,'FCM already exists with this project Id!')
            return redirect('credentials:firebase_credentials_list')
        FirebaseCredentials.objects.create(
            fcm_file = request.FILES.get('fcm_file'),
            project_id = request.POST.get('project_id'),
        )
        messages.success(request,'FCM file added successfully!')
        return redirect('credentials:firebase_credentials_list')

class ViewFirebaseKeys(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        firebase_credentials = FirebaseCredentials.objects.get(id=self.kwargs['id'])
        return render(request,'credentials/firebase/view-credentials.html',{
            'head_title':'Firebase Management',
            'firebase_credential':firebase_credentials, 
        })

class ActivateFirebaseStatus(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        firebase_credentials = FirebaseCredentials.objects.get(id=self.kwargs['id'])
        if firebase_credentials.active:
            firebase_credentials.active = False
            message = 'Deactivated Successfully!'
        else:
            FirebaseCredentials.objects.all().update(active=False)
            firebase_credentials.active = True
            message = 'Activated Successfully!'
        firebase_credentials.save()
        messages.success(request,message)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class UpdateFirebaseKeys(View):
    @method_decorator(admin_only)
    def post(self,request,*args,**kwargs):
        firebase_credentials = FirebaseCredentials.objects.get(id=request.POST.get('key_id'))
        if FirebaseCredentials.objects.filter(fcm_file = request.FILES.get('fcm_file')).exclude(id=request.POST.get('key_id')):
            messages.error(request,'Key already exists!')
            return redirect('credentials:view_firebase_credentials',id=request.POST.get('key_id'))
        if request.FILES.get('fcm_file'):
            firebase_credentials.fcm_file = request.FILES.get('fcm_file')
        if request.POST.get('project_id'):
            firebase_credentials.project_id = request.POST.get('project_id')
        firebase_credentials.save()
        messages.success(request,'Fcm file updated successfully')
        return redirect('credentials:view_firebase_credentials',id=request.POST.get('key_id'))

class DeleteFirebase(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        FirebaseCredentials.objects.get(id=self.kwargs['id']).delete()
        messages.success(request,'Firebase credentials deleted successfully!')
        return redirect('credentials:firebase_credentials_list')
    

"""
Stripe Credentials Management
"""
class StripeSettingList(View):
    """
    Stripe Keys List
    """
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        keys = StripeSetting.objects.all().order_by('-created_on')
        keys = query_filter_constructer(request, keys,
            {
                "test_publishkey__icontains": "publish_key",
                "test_secretkey__icontains": "secret_key",
                "active": "status",
                "created_on__date": "created_on",
            })
        if not keys and request.GET:
            messages.error(request, 'No Data Found')
        return render(request,'credentials/stripe-keys/stripe-keys.html',{
            'head_title':'Stripe Management',
            'keys':keys
        })
    
    @method_decorator(admin_only)
    def post(self, request, *args, **kwargs):
        if int(len(StripeSetting.objects.all())) >= MAX_PROVIDERS_KEY:
            messages.error(request,f'Sorry ,Maximum {MAX_PROVIDERS_KEY} Keys can be added')
            return redirect('credentials:stripe_keys')
        StripeSetting.objects.create(test_publishkey=request.POST.get('publish_key'),test_secretkey=request.POST.get('secret_key'))
        return redirect('credentials:stripe_keys')
    

class EditStripeSetting(View):
    """
    Edit Stirpe Keys
    """
    @method_decorator(admin_only)
    def post(self, request, *args, **kwargs):
        keys = StripeSetting.objects.get(id=request.POST.get('key_id'))
        if request.POST.get('publish_key'):
            keys.test_publishkey = request.POST.get('publish_key')
        if request.POST.get('secret_key'):
            keys.test_secretkey = request.POST.get('secret_key')
        keys.save()
        return redirect('credentials:stripe_keys')

class ViewStripeSetting(View):
    """
    View Stripe Keys
    """
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        key = StripeSetting.objects.get(id=self.kwargs['id'])
        return render(request, 'credentials/stripe-keys/view-stripe-keys.html',{
            "key":key,
            "head_title":"Stripe Management",
            })

class DeleteStripeSetting(View):
    """
    Delete Stripe Keys
    """
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        StripeSetting.objects.get(id=self.kwargs['id']).delete()
        messages.success(request, 'Keys deleted successfully!')
        return redirect('credentials:stripe_keys')
    
class ChangeStripeStatus(View):
    """
    Change Stripe Status
    """
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        key = StripeSetting.objects.get(id=self.kwargs['id'])
        if key.active:
            key.active=False
            messages.success(request,'Key deactivated successfully!')
        else:
            StripeSetting.objects.all().update(active = False)
            key.active = True   
            messages.success(request,'Key activated auccessfully!')
        key.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))