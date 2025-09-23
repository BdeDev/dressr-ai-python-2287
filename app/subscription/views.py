from django.shortcuts import render
from accounts.common_imports import *
from .models import *


class ListSubscriptionPlan(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        subscription_plans = SubscriptionPlans.objects.all().order_by('-created_on')
        subscription_plans = query_filter_constructer(request,subscription_plans,{
            "title__icontains":"title",
            "price":"price",
            "final_price":"final_price",
            "month_year":"month_year",
            "validity":"validity",
            "status":"status",
        })
        if request.GET and not subscription_plans:
            messages.error(request, 'No Data Found')
        return render(request,'subscription/plan-list.html',{
            "head_title":'Subscription Plan Management',
            "subscription_plans" : get_pagination(request, subscription_plans),
            "scroll_required":True if request.GET else False,
            "total_objects":subscription_plans.count()
        })
    
class AddSubscriptionPlan(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        return render(request,'subscription/add-plan.html',{"head_title":'Subscription Plan Management'})
    
    @method_decorator(admin_only)
    def post(self,request,*args,**kwargs):
        title = request.POST.get('title').strip()
        month_year = int(request.POST.get('month_year').strip())
        validity = YEARLY_PLAN
        price = float(request.POST.get('price').strip())
        final_price = price * (month_year * 12) ## price * year * 12 (number of month in year)
        final_price = round(final_price,2)

        if SubscriptionPlans.objects.filter(validity=validity,month_year=month_year,is_deleted=False).exists():
            messages.success(request, "Subscription plan already exists")
            return redirect('subscription:add_subscription_plan')
        
        plan = SubscriptionPlans.objects.create(
            title = title,
            month_year = month_year,
            validity = validity,
            features = request.POST.get('description',None),
            price = price,
            final_price = final_price,
            created_by = request.user,
            status = False,
            max_uploads = request.POST.get('max_uploads'),
            max_try_ons = request.POST.get('max_try_ons'),
            max_shares = request.POST.get('max_shares'),
        )
        messages.success(request, "Subscription plan added successfully!")
        return redirect('subscription:view_plan',plan.id)

class ViewSubscriptionPlan(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        plan = SubscriptionPlans.objects.get(id=self.kwargs['id'])
        return render(request, 'subscription/view-plan.html',{
            "head_title":"Subscription Plans Management",
            "plan":plan,
        })

class EditSubscriptionPlan(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        plan = SubscriptionPlans.objects.get(id=self.kwargs['id'])
        return render(request,'subscription/edit-plan.html',{
            'head_title':'Subscription Plans Management',
            'plan':plan
        })
    @method_decorator(admin_only)
    def post(self,request,*args,**kwargs):
        plan = SubscriptionPlans.objects.get(id=self.kwargs['id'])
        title = request.POST.get('title').strip()
        month_year = int(request.POST.get('month_year').strip())
        validity = YEARLY_PLAN
        price = float(request.POST.get('price').strip())
        final_price = price * (month_year * 12) ## price * year * 12 (number of month in year)
        final_price = round(final_price,2)

        if SubscriptionPlans.objects.filter(validity=validity,month_year=month_year,is_deleted=False).exclude(id=plan.id):
            messages.error(request,"Subscription plan already exists ")
            return redirect('subscription:edit_plan',id=plan.id)
        else:
            plan.title = title
            plan.month_year=month_year     
            plan.price = price
            plan.final_price = final_price
            plan.validity = validity 
            plan.features=request.POST.get('description',None)
            plan.max_uploads = request.POST.get('max_uploads')
            plan.max_try_ons = request.POST.get('max_try_ons')
            plan.max_shares = request.POST.get('max_shares')
            plan.save()
            messages.success(request, "Plan updated successfully!")
        return redirect('subscription:view_plan',plan.id)

class DeleteSubscriptionPlan(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        plan=SubscriptionPlans.objects.get(id=self.kwargs['id'])
        if UserPlanPurchased.objects.filter(subscription_plan=plan):
            messages.error(request, "Plan cannot be deleted because it is being used by the customer")
            return redirect('subscription:all_plans')
        plan.is_deleted = True
        plan.save()
        messages.success(request, "Plan deleted successfully!")
        return redirect('subscription:all_plans')
    
class SubscriptionPlanStatus(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        subscription_plan = SubscriptionPlans.objects.get(id=self.kwargs['id'])
        if subscription_plan.status:
            subscription_plan.status = False
            message="Notification Deactivated Successfully!"
        else:
            subscription_plan.status = True
            message="Notification Activated Successfully!"
        subscription_plan.save()
        messages.success(request,message=message)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    

"""
Purchased plan 
"""
class PluchasedPlanList(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        plan_user = User.objects.filter(id=request.GET.get('to_user')).last()
        plans = UserPlanPurchased.objects.all().order_by('status','-created_on')
        plans = query_filter_constructer(request,plans,
            {
                "plan_id__icontains":"plan_id",
                "final_amount":"final_amount",
                "status":"status",
                "created_on__date":"created_on",
                "purchased_by_id":"to_user"
            }
        )
        if request.GET.get('created_by'):
            plans = plans.filter(
                Q(purchased_by__full_name__icontains = request.GET.get('created_by'))|
                Q(purchased_by__bank_name__icontains = request.GET.get('created_by'))
                )
        if request.GET and not plans:
            messages.error(request, 'No data found!')
        return render(request, "subscription/purchased-plan/purchased-plans.html",{
            "head_title":"Purchased Plans",
            "plans": get_pagination(request, plans),
            "search_filters":request.GET.copy(),
            "total_objects":plans.count(),
            "plan_user":plan_user,
        })
    


class PurchasedPlanInfo(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        plan = UserPlanPurchased.objects.get(id=self.kwargs['id'])
        user = plan.purchased_by
        return render(request, "subscription/purchased-plan/plans-details.html",{
            "head_title":"Purchased Plans",
            "plan": plan,
            "user":user,
        })

class ActivatePurchasedPlanNow(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        purchase_plan = UserPlanPurchased.objects.get(id=self.kwargs['id'],status= USER_PLAN_IN_QUEUE)
        user = purchase_plan.purchased_by
        ## mark activate plan expire 
        UserPlanPurchased.objects.filter(
            purchased_by=user,
            status=USER_PLAN_ACTIVE
            ).update(
            status=USER_PLAN_EXPIRED,
            marked_expired_by = request.user
            )
        
        user.is_subscription_active = False
        user.save()
        user.refresh_from_db()
        ## create and activate plan 
        activate_subscription(user,purchase_plan)
        messages.success(request,'Plan activated successfully')

        if purchase_plan.month_year > 1:
            title = f"Subscription plan for {purchase_plan.month_year} years activated"
            description = f"Subscription plan for {purchase_plan.month_year} years activated by admin "
        else:
            title = f"Subscription plan for {purchase_plan.month_year} year activated"
            description = f"Subscription plan for {purchase_plan.month_year} year activated by admin "
        
        ## send notification to admin
        # send_notification(
        #     created_by = request.user,
        #     created_for = [user],
        #     title = title,
        #     description =  description,
        #     notification_type = NOTIFICATION_SUBSCRIPTION,
        #     obj_id = str(purchase_plan.id),
        # )

        return redirect('subscriptions:purchased_plan_info',id=purchase_plan.id)