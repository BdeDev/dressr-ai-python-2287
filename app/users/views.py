from accounts.common_imports import *
from django.contrib.auth.hashers import make_password
from django.contrib.sites.models import Site
from django.db.models.functions import Concat
from django.contrib.auth import logout
from ecommerce.models import AffiliateSettings
from wardrobe.models import *
from accounts.stripe_views import *
import re

@method_decorator(admin_only,name='dispatch')
class EditAdmin(View):
    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=self.kwargs['id'])
        if not user.role_id in [ADMIN]:
            messages.error(request,"Sorry! You have no permissions to do this task.")
            return redirect("frontend:index")
        return render(request, 'admin/edit-admin.html',{"head_title":"Admin Profile","user":user})

    def post(self, request, *args, **kwargs):
        user = User.objects.get(id=self.kwargs['id'])
        username = request.POST.get("username")
        username_users = User.objects.filter(Q(status = ACTIVE)|Q(status = INACTIVE), username=username).exclude(id=self.kwargs['id'])

        if username_users:
            messages.success(request,"Username already exists")
            return render(request, 'admin/edit-admin.html',{"head_title":"Admin Profile","user":user}) 

        user.username = username
        user.full_name = username.capitalize()

        if request.FILES.get('profile_pic'):
            user.profile_pic = request.FILES.get('profile_pic')
        user.save()
        messages.success(request,"Profile updated successfully!")
        return redirect('users:view_user',id=user.id)

class ViewUser(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=self.kwargs['id'])
        
        if user.role_id == ADMIN:
            login_history = LoginHistory.objects.filter(user_email=user.email).order_by('-created_on').only('id')
            if not request.user.role_id == ADMIN:
                return render(request, 'frontend/restrict.html')
            site=Site.objects.first()
            return render(request, 'admin/admin-profile.html', {"user":user,"site":site,"head_title":"Admin Profile"})
        elif user.role_id == CUSTOMER:
            login_history = LoginHistory.objects.filter(user_email=user.email).order_by('-created_on').only('id')
            device = Device.objects.filter(user=user).last()
            outfits = Outfit.objects.filter(created_by = user).order_by('-created_on')
            return render(request, 'users/users/user-profile.html', {
                "head_title":"User Management",
                "isCustomer":True,
                "user":user,
                "device":device,
                "token":Token.objects.filter(user=user).last(),
                'loginhistory':get_pagination(request,login_history),
                'wardrobe':Wardrobe.objects.filter(user=user).first(),
                "outfits":get_pagination(request,outfits),
                "item_count":ClothingItem.objects.filter(wardrobe__user=user).count(),
                "favourite_items":get_pagination(request,user.favourite_item.all()),
                "virtual_tryons":get_pagination(request,VirtualTryOn.objects.filter(user=user))
            })
        
        elif user.role_id == AFFILIATE:
            login_history = LoginHistory.objects.filter(user_email=user.email).order_by('-created_on').only('id')
            return render(request, 'users/affiliate/affiliate-profile.html', {
                "head_title":"Affiliate Management",
                "isCustomer":False,
                "user":user,
                'loginhistory':get_pagination1(request,login_history,1),
            })
        else:
            logout(request)
            return redirect('frontend:index')


class InactivateUser(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=self.kwargs['id'])
        if request.user == user:
            return render(request, 'frontend/restrict.html')
        user.status = INACTIVE
        user.save()
        Token.objects.filter(user=user).delete()
        messages.success(request,'Account deactivated successfully!')
        bulk_send_user_email(
            request, user, 'EmailTemplates/AccountStatus.html',
            'Account Deactivated', user.email, "", "Your account has been deactivated. Please contact admin to activate your account.",
            'Account Deactivated', "",assign_to_celery=False)
        return redirect('users:view_user',id=user.id)


class DeleteUser(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=self.kwargs['id'])
        if request.user == user:
            return render(request, 'frontend/restrict.html')
        
        user.status = DELETED
        Token.objects.filter(user=user).delete()
        if user.username:
            user.username = user.username + str(user.id)
        user.save()

        messages.success(request,'Account deleted successfully!')
        bulk_send_user_email(request, user, 'EmailTemplates/AccountStatus.html', 'Account Deleted', user.email, "", "Your account has been deleted. Please contact admin to activate your account.", 'Account Deleted', "",assign_to_celery=False)
        return redirect('users:view_user',id=user.id)


class ActivateUser(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=self.kwargs['id'])
        if request.user == user:
            return render(request, 'frontend/restrict.html')
        user.status = ACTIVE
        user.save()
        messages.success(request,'Account activated successfully!')
        bulk_send_user_email(request, user, 'EmailTemplates/AccountStatus.html', 'Account Activated', user.email, "", "Your account has been activated.", 'Account Activated', "",assign_to_celery=False)
        return redirect('users:view_user',id=user.id)


class UsersList(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        users = User.objects.filter(role_id=CUSTOMER).order_by('-created_on')
        users = query_filter_constructer(request,users,
                {
                    "username__icontains":"username",
                    "full_name__icontains":"full_name",
                    "email__icontains":"email",
                    "created_on__date":"created_on",
                    "status":"status"
                }
            )
        if request.GET.get('mobile_no'):
            users = users.annotate(full_mobile=Concat('country_code', 'mobile_no')).filter(full_mobile__icontains=request.GET.get('mobile_no'))

        if request.GET and not users:
            messages.error(request, 'No Data Found')
        return render(request,'users/users/users-list.html',{
            "head_title":'User Management',
            "users" : get_pagination(request, users),
            "scroll_required":True if request.GET else False,
            "total_objects":users.count()
        })


## ---------------------Affiliate Management------------------------

class AffiliateList(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        affiliates = User.objects.filter(role_id=AFFILIATE).order_by('-created_on')
        affiliates = query_filter_constructer(request,affiliates,
                {
                    "username__icontains":"username",
                    "full_name__icontains":"full_name",
                    "email__icontains":"email",
                    "created_on__date":"created_on",
                    "status":"status"
                }
            )
     
        if request.GET.get('mobile_no'):
            affiliates = affiliates.annotate(full_mobile=Concat('country_code', 'mobile_no')).filter(full_mobile__icontains=request.GET.get('mobile_no'))
        
        if request.GET and not affiliates:
            messages.error(request, 'No Data Found')

        return render(request,'users/affiliate/affiliate-list.html',{
            "head_title":'Affiliate Management',
            "affiliates" : get_pagination(request, affiliates),
            "scroll_required":True if request.GET else False,
            "total_objects":affiliates.count()
        })

class AddAffiliate(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        return render(request, 'users/affiliate/add-affiliate.html', {
            'head_title': "Affiliate Management",
        })
    @method_decorator(admin_only)
    def post(self, request, *args, **kwargs):
        email = request.POST.get("email").strip()
        mobile_no = request.POST.get("mobile_no").strip()

        # Check for existing user
        if User.objects.filter(email=email, role_id =AFFILIATE, status__in=[ACTIVE, INACTIVE]).exists():
            messages.error(request, 'Affiliate already exists with this email id.')
            return redirect('users:add_affiliate')

        if User.objects.filter(mobile_no=mobile_no, role_id=AFFILIATE, status__in=[ACTIVE, INACTIVE]).exists():
            messages.error(request, 'User already exists with this mobile number')
            return redirect('users:add_affiliate')


        if request.POST.get('password'):
            check = re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',request.POST.get('password'))
            if not check:
                messages.error(request, 'Password must contain at least 8 characters, including uppercase, lowercase, numbers, and special characters')
                return redirect('users:add_affiliate')
                    
        email_first = request.POST.get('email').split('@')
        email_first = email_first[0]
        suggestions = generate_mydressr_username(email_first)
        username = suggestions[0]
        try:
            user = User.objects.create(
                first_name=request.POST.get('first_name').strip(),
                last_name=request.POST.get('last_name').strip(),
                username = username,
                email=email,
                role_id=AFFILIATE,
                gender=request.POST.get('gender'),
                country_code=request.POST.get('country_code'),
                country_iso_code=request.POST.get('country_iso_code'),
                mobile_no=mobile_no,
                profile_pic=request.FILES.get('profile_pic'),
                password=make_password(request.POST.get('password')),
                status=ACTIVE,
                referral_code = GenerateReferal(),
            )
            user.full_name = user.first_name + " " + user.last_name
            user.save()
            messages.success(request, 'Affiliate created successfully !')
            # bulk_send_user_email(request, user, "EmailTemplates/login-crenditials.html", 'Login credentials', user.email, request.POST.get("password"), '', '', '',assign_to_celery=False)
            return redirect('users:affiliate_list')
        except Exception as e:
            messages.error(request, 'Failed to create user.')
            return redirect('users:add_affiliate')


class EditAffiliate(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        affiliate = User.objects.get(id=self.kwargs['id'])
        return render(request, 'users/affiliate/edit-affiliate.html', {
            "head_title": "Affiliate Management",
            "affiliate": affiliate,
            'GOOGLE_PLACES_KEY': env('GOOGLE_PLACES_KEY')
        })
    @method_decorator(admin_only)
    def post(self, request, *args, **kwargs):
        user = User.objects.get(id=self.kwargs['id'])
        email = request.POST.get("email").strip()

        # Check for existing user
        if User.objects.filter(email=email, role_id=AFFILIATE, status__in=[ACTIVE, INACTIVE]).exclude(id=user.id).exists():
            messages.error(request, 'User already exists with this email id.')
            return redirect('users:edit_affiliate',id=user.id)

        if User.objects.filter(role_id=AFFILIATE, status__in=[ACTIVE, INACTIVE]).exclude(id=user.id).exists():
            messages.error(request, 'User already exists with this mobile no')
            return redirect('users:edit_affiliate',id=user.id)

        if request.FILES.get('profile_pic'):
            user.profile_pic = request.FILES.get('profile_pic')

        if request.POST.get("first_name"):
            user.first_name = request.POST.get("first_name").strip()
        if request.POST.get("last_name"):
            user.last_name = request.POST.get("last_name").strip()

        user.full_name = user.first_name + " " + user.last_name
        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('users:view_user', id=user.id)

class UpdateAffiliateCommission(View):
    @method_decorator(admin_only)
    def post(self, request, *args, **kwargs):
        affiliate_commission = AffiliateSettings.objects.get(affiliate=self.kwargs['id'])
        
        commission_percentage = request.POST.get('commission_percentage')
        transactions = request.POST.get('transactions')
        minimum_payment_threshold = request.POST.get('minimum_payment_threshold')

        affiliate_commission.Commission_percentage = float(commission_percentage) if commission_percentage else 0
        affiliate_commission.number_of_transactions = int(transactions) if transactions else 0
        affiliate_commission.minimum_payment_threshold = float(minimum_payment_threshold) if minimum_payment_threshold else 0

        affiliate_commission.save()
        messages.success(request, 'Commission setting updated successfully!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
# class ModifyAffiliateStipeAccount(View):
#     @method_decorator(admin_only)
#     def get(self,request,*args,**kwargs):
#         user = User.objects.get(id=self.kwargs['id'])
#         type = request.GET.get('type')
#         if type not in ['customer','account']:
#             messages.error(request, 'Invalid Request')
#             return redirect(request.META.get('HTTP_REFERER'))
        
#         if type == 'customer' and not user.customer_id:
#             is_created = CreateStripeCustomer(request,user)
#             if is_created:
#                 messages.success(request, 'Stripe customer created successfully')
#             else:
#                 messages.error(request, 'Failed to create stripe customer')
#         elif type == 'account' and not user.account_id:
#             is_created = create_connected_account(user)
#             if is_created:
#                 messages.success(request, 'Stripe account created successfully')
#             else:
#                 messages.error(request, 'Failed to create stripe account')
#         else:
#             messages.error(request, 'Stripe ID already exists')

#         return redirect(request.META.get('HTTP_REFERER'))

class NotificationOnOff(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        user = User.objects.get(id=self.kwargs['id'])
        if user.notification_enable:
            user.notification_enable = False
            message="Notification Deactivated Successfully!"
        else:
            user.notification_enable = True
            message="Notification Activated Successfully!"
        user.save()
        messages.success(request,message=message)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class EmailNotificationOnOff(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        user = User.objects.get(id=self.kwargs['id'])
        if user.email_notification:
            user.email_notification = False
            message="Email Notification Deactivated Successfully!"
        else:
            user.email_notification = True
            message="Email Notification Activated Successfully!"
        user.save()
        messages.success(request,message=message)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class DeleteUsers(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        user  = User.objects.get(id = self.kwargs.get('id'))
        user.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
