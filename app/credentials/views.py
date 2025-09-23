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