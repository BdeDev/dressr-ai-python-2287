import re
import subprocess
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.sites.models import Site
from cron_descriptor import get_description
from .decorators import *
from django.views.generic import TemplateView,View
from accounts.management.commands.hair_color import default_hair_colors
from accounts.models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from accounts.common_imports import *
from accounts.utils import *
from rest_framework.authtoken.models import Token


db_logger = logging.getLogger('db')
env = environ.Env()
environ.Env.read_env()


class AdminLoginView(TemplateView):
    def get(self, request, *args, **kwargs):
        return redirect('accounts:login')

class LogOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect('accounts:login')

class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('frontend:index')
        return render(request, 'registration/login.html', {'next': request.GET.get('next')})

    def post(self, request, *args, **kwargs):
        username = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()
        remember_me = request.POST.get('remember_me') == 'on'

        # Handle missing fields
        if not username or not password:
            messages.error(request, "Please enter both email and password.")
            return render(request, 'registration/login.html', {"username": username, "password": password})

        # Authenticate user
        user = authenticate(username=username, password=password)
        if not user:
            messages.error(request, 'Invalid login details.')
            return render(request, 'registration/login.html', {"email": username, "password": password})

        # Check allowed roles
        if user.is_superuser and user.role_id == ADMIN:
            login(request, user)
            if remember_me:
                request.session.set_expiry(1209600)
            messages.success(request, "Logged in successfully!")
            redirect_url = request.GET.get('next','admin:index') 
            return redirect(redirect_url)

        # Unauthorized role
        messages.error(request, 'Invalid login details.')
        return render(request, 'registration/login.html', {"username": username, "password": password})


class PasswordChange(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        return render(request,'admin/change-password.html',{"head_title":"Change Password"})

    def post(self,request,*args,**kwargs):
        user = User.objects.get(id=request.user.id)
        if not user.check_password(request.POST.get('current_password')):
            messages.error(request, 'Current Password does not match')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if request.POST.get('current_password') == request.POST.get("password"):
            messages.error(request, 'New password must be different from the current password!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        user.set_password(request.POST.get("password"))
        user.save()
        messages.success(request, 'Password changed successfully')
        return redirect('frontend:index')


def Validations(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data ={"valid":None,"email":False, "username":False,"mobile_no":False}

        email = request.GET.get('email')
        username = request.GET.get('username')
        mobile_no = request.GET.get('mobile_no')
        if email:
            match = str(re.search(r'^[a-zA-Z0-9_.+-]+[@]\w+[.]\w{2,3}$',email.strip()))    

            if match != "None":
                data['valid'] = '1'
            else:
                data['valid'] = '0'

        user_filter = User.objects.filter(status__in=[ACTIVE, INACTIVE, DELETED])
        if request.GET.get('id'):
            user = User.objects.get(id=request.GET.get('id'))
            if email:
                data['email'] = user_filter.filter(email=email).exclude(id=user.id).exists()
            if username:
                data['username'] = user_filter.filter(username=username).exclude(id=user.id).exists()
            if mobile_no:
                data['mobile_no'] = user_filter.filter(mobile_no=mobile_no).exclude(id=user.id).exists()
        else:
            if email:
                data['email'] = user_filter.filter(email=email).exists()
            if username:
                data['username'] = user_filter.filter(username=username).exists()
            if mobile_no:
                data['mobile_no'] = user_filter.filter(mobile_no=mobile_no).exists()
        return JsonResponse(data)


"""
Password Management
"""

class ResetPassword(View):
    def get(self, request, *args, **kwargs):
        uid = kwargs.get('uid')
        token_key = kwargs.get('token')
        user = get_object_or_404(User, id=uid)
        try:
            token = Token.objects.get(key=token_key, user=user)
            return render(request, 'registration/ResetPassword.html', {"token": token, "uid": uid})
        except Exception as e:
            return render(request, 'frontend/failed-verification.html',{'protocol': 'https' if USE_HTTPS else 'http', 'domain': env('SITE_DOMAIN')})
      

    def post(self, request, *args, **kwargs):
        uid = kwargs.get('uid')
        token_key = kwargs.get('token')
        password = request.POST.get("password").strip()
        try:
            user = get_object_or_404(User, id=uid)
            token = Token.objects.get(key=token_key, user=user)

            if not password:
                messages.error(request, 'Password is required.')
                return render(request, 'registration/ResetPassword.html', {"token": token, "uid": uid})

            user.set_password(password)
            user.save()
            token.delete()
            return render(request,'frontend/password-reset-successful.html', {
                    "user": user, 'protocol': 'https' if USE_HTTPS else 'http', 'domain': env('SITE_DOMAIN')})
        except:
            return render(request, 'registration/ResetPassword.html', {"token": token, "uid": uid})
      


class ForgotPasswordEmail(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'registration/forgot-email.html')

    def post(self, request, *args, **kwargs):
        if not User.objects.filter(Q(status=ACTIVE)|Q(status=INACTIVE),email=request.POST.get("email")).exists():
            messages.success(request,'Please enter a registered email address.')
            return redirect('accounts:forgot_password_email')
        else:
            user = User.objects.get(email=request.POST.get("email"))
            token, _ = Token.objects.get_or_create(user_id=user.id)
            reset_path = reverse("accounts:reset_password_user", kwargs={"uid": user.id, "token": token})
            reset_link = request.build_absolute_uri(reset_path)
            # Send reset link via email
            bulk_send_user_email(request,user,'EmailTemplates/reset_password_admin.html','Reset Your Password',request.POST.get("email"),reset_link,"","","",assign_to_celery=False)
            messages.success(request,'A link has been sent on your email to reset your password.')
            return redirect('accounts:login')


"""
Verify Account through email 
"""
class VerifyUserAccount(View):
    def get(self, request, *args, **kwargs):
        try:
            user_otp = request.GET.get('otp')
            token = Token.objects.get(key=self.kwargs.get('token'))
            user = User.objects.get(id=token.user_id)
            if user.temp_otp == user_otp:
                user.is_verified = True
                user.save()
                token.delete()
                return render(request,'frontend/success-verification.html',{"user":user,'protocol': 'https' if USE_HTTPS else 'http','domain':env('SITE_DOMAIN')})
            token.delete()
            return render(request,'frontend/failed-verification.html',{'protocol': 'https' if USE_HTTPS else 'http','domain':env('SITE_DOMAIN')})
        except:
            return render(request,'frontend/failed-verification.html',{'protocol': 'https' if USE_HTTPS else 'http','domain':env('SITE_DOMAIN')})

"""
Notification Management
"""
class NotificationsList(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=self.kwargs.get('id'))
        notifications = Notifications.objects.filter(created_for=user).order_by('-created_on')
        return render(request, "admin/notifications.html",{
            "head_title": "Notifications Management",
            "notifications": get_pagination(request,notifications),
            "total_objects": notifications.count(),
            "user":user
        })


class DeleteNotifications(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        notifications = Notifications.objects.filter(created_for__role_id=ADMIN)
        if notifications:
            notifications.delete()
            messages.success(request, 'Notifications deleted successfully!')
        else:
            messages.error(request, "No notifications to delete!")
        return redirect('accounts:notifications_list',request.user.id)


class MarkReadNotifications(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=self.kwargs.get('id'),role_id = ADMIN)
        notifications = Notifications.objects.filter(created_for=user).order_by('-created_on')
        if notifications:
            notifications.update(is_read=True)
            messages.success(request, 'All notifications marked as read successfully!')
        else:
            messages.error(request, "No Notifications to Read!")
        return redirect('accounts:notifications_list',id=user.id)


'''
CronJob Management
'''
class ListCronjob(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        cron1, id, name, time, days = [], [], [], [], []
        try:
            crons=subprocess.run(['python3', 'manage.py', 'crontab', 'show'], stdout=subprocess.PIPE)
            if crons:
                crons=crons.stdout.decode().split(':')[1].replace('->',',').replace('.',' ').replace("'","").replace("\"","").replace('(','').replace(')','').strip().split('\n')
                for x in crons:
                    cron1.append(x.split(','))
                for x in cron1:
                    if len(x) == 3:
                        id.append(x[0].strip())
                        time.append(x[1].strip())
                        name.append(x[2].strip())
                cron1.clear()
                for x in name:
                    cron_name = x.split(' ')[::-1][0]
                    cron1.append(cron_name)
                for x in time:
                    cron=get_description(x)
                    days.append(cron)
                crontabs=list(zip(id, cron1, days, time))
        except subprocess.CalledProcessError as e:
            crons=f'Command {e.cmd} failed with error {e.returncode}'    
        return render(
            request, 'admin/cronjobs.html', {'head_title': 'Cronjob Management', 'crontab': crontabs}
            )


class AddCronjob(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        os.system('python3 manage.py crontab remove')
        os.system('python3 manage.py crontab add')
        messages.success(request, 'Cronjobs added successfully')
        return redirect('accounts:list_cronjob')


class RemoveCronjob(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        os.system('python3 manage.py crontab remove')
        messages.success(request, 'Cronjobs removed successfully')
        return redirect('accounts:list_cronjob')


class RunCronjob(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        os.system(f"python3 manage.py crontab run {self.kwargs.get('id')}")
        messages.success(request, 'Cronjob ran Successfully!')
        return redirect('accounts:list_cronjob')


"""
Login History Management
"""

class LoginHistoryView(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        loginhistory = LoginHistory.objects.all().order_by('-created_on')
        loginhistory = query_filter_constructer(
            request, loginhistory,
            {
                "user_email__icontains": "email",
                "user_ip__icontains": "user_ip",
                "user_agent__icontains": "agent",
                "status": "status",
                "url__icontains": "url",
                "created_on__date": "created_on",
            })

        if not loginhistory and request.GET:
            messages.error(request, 'No Data Found')
        return render(request, 'admin/login-history.html', {
            "head_title":"Login History Management",
            "loginhistory": get_pagination(request, loginhistory),
            "search_filters":request.GET.copy(),
            "total_objects": loginhistory.count(),
        })
class DeleteHistory(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        deleted_count, _ = LoginHistory.objects.all().delete()
        if deleted_count:
            messages.success(request, "All login history cleared successfully!")
        else:
            messages.error(request, "Nothing to delete!")
        return redirect('accounts:login_history')


class SendBulkNotification(View):
    @method_decorator(admin_only)
    def post(self, request, *args, **kwargs):
        super_admin=User.objects.filter(is_superuser=True, role_id=ADMIN).first()
        users=User.objects.all()
        messages.success(request, "Successfully notified all users with your message.")
        bulk_send_notification(
            created_by= super_admin,
            created_for=[user for user in users],
            title=f'Admin Message',
            description=request.POST.get('message').strip(),
            notification_type=ADMIN_NOTIFICATION,
            obj_id= "",
        )
        return redirect('users:view_user', id=super_admin.id)



class UpdateDjangoSite(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        site=Site.objects.first()
        return render(request,'admin/site-setting.html',{
            "head_title":'Domain Management',
            "site":site
        })
    @method_decorator(admin_only)
    def post(self, request, *args, **kwargs):
        site = Site.objects.first()
        site.domain = request.POST.get('domain').strip()
        site.name = request.POST.get('domain').strip()
        site.save()

        messages.success(request,'Domain information updated successfully.')
        return redirect('accounts:update_django_site')



class ImportHairColorView(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        for color in default_hair_colors:
            obj, created = HairColor.objects.get_or_create(
                title=color["name"],
                defaults={
                    "color_code": color["hex"],
                }
            )
            if created:
                messages.success(request,f"Added hair color: {color['name']}")
            else:
                messages.error(request,f"Hair color already exists: {color['name']}")
        return redirect('seatmap:charts_list')
    

class ImportSkinToneView(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        for color in default_hair_colors:
            obj, created = HairColor.objects.get_or_create(
                title=color["name"],
                defaults={
                    "color_code": color["hex"],
                }
            )
            if created:
                messages.success(request,f"Added hair color: {color['name']}")
            else:
                messages.error(request,f"Hair color already exists: {color['name']}")
        return redirect('seatmap:charts_list')
    
## Banner Management

class BannersList(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        banners = Banners.objects.all().order_by('-updated_on').only('id')
        banners  = query_filter_constructer(request,banners,{
            "title__icontains":"title",
            "is_active":"state",
            "created_on__date":"created_on"
        })
        if request.GET and not banners:
            messages.error(request, 'No data found')
        return render(request, 'ecommerce/banners/banner-list.html',{
            "banners":get_pagination(request, banners),
            "search_filters":request.GET.copy(),
            "head_title":"Banners Management",
        })
    
    @method_decorator(admin_only)
    def post(self, request,*args,**kwargs):
        banner_id = request.POST.get('banner_id')
        if banner_id:
            banner = get_or_none(Banners,'Banner does not exist !',id=banner_id)
            if Banners.objects.filter(title=request.POST.get('title')).exclude(id=banner_id).exists():
                messages.error(request, "Banner already exists!")
                return redirect('accounts:banners_list')
            if request.POST.get('title'):
                banner.title = request.POST.get('title').strip()
            if request.FILES.get('image'):
                banner.image = request.FILES.get('image')
            banner.save()
            messages.success(request, "Banner updated successfully!")
        else:
            if Banners.objects.filter(title=request.POST.get('title')).exists():
                messages.error(request, "Banner already exists!")
                return redirect('accounts:banners_list')
            if request.FILES.get('image'):
                Banners.objects.create(
                    title = request.POST.get('title'),
                    image = request.FILES.get('image',None),
                    is_active = False if Banners.objects.filter(is_active=True).count() >= MAX_ACTIVE_BANNER else True,
                )
                messages.success(request, "Banner added successfully!")
        return redirect('accounts:banners_list')
    

class ChangeBannerStatus(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        banner = Banners.objects.get(id=self.kwargs['id'])
        if banner.is_active:
            banner.is_active = False
            message = "Banner Deactivated Successfully!"
        else:
            if Banners.objects.filter(is_active=True).count() >= MAX_ACTIVE_BANNER:
                messages.success(request,f'Sorry ,Maximum {MAX_ACTIVE_BANNER} banner could be activated at same time!')
                return redirect('accounts:banners_list')
            banner.is_active = True
            message = "Banner Activated Successfully!"
        banner.save()
        messages.success(request,message)
        return redirect('accounts:banners_list')
    

class DeleteBanner(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        Banners.objects.get(id=self.kwargs['id']).delete()
        messages.success(request,'Banner Deleted Successfully!')
        return redirect('accounts:banners_list')
