from .views import *
from django.contrib import admin
from django.urls import re_path
from .views_api import *

admin.autodiscover()
app_name = 'subscription'

urlpatterns = [


    ## Subscription Plans
    re_path(r'^subscription-plans-list/$', ListSubscriptionPlan.as_view(), name='all_plans'),
    re_path(r'^add-subscription-plan/$', AddSubscriptionPlan.as_view(), name='add_subscription_plan'),
    re_path(r'^view-subscription-plan/(?P<id>[-\w]+)/',ViewSubscriptionPlan.as_view(),name="view_plan"),
    re_path(r'^edit-plan/(?P<id>[-\w]+)/$',EditSubscriptionPlan.as_view(), name='edit_plan'),
    re_path(r'^delete-plan/(?P<id>[-\w]+)/$',DeleteSubscriptionPlan.as_view(), name='delete_plan'),
    re_path(r'^change-status/(?P<id>[-\w]+)/$',SubscriptionPlanStatus.as_view(), name='change_status'),

    ## Purchased Plans
    re_path(r'^purchased-plans/$',PluchasedPlanList.as_view(),name="purchased_plans"),
    re_path(r'^purchased-plan-info/(?P<id>[-\w]+)/$', PurchasedPlanInfo.as_view(), name='purchased_plan_info'),
    re_path(r'^activate-plan/(?P<id>[-\w]+)/$', ActivatePurchasedPlanNow.as_view(), name='activate_plan'),

    ## Subscription Plans APIs
    re_path(r'^subscriptions-list/$', SubscriptionPlansListing.as_view(), name='subscriptions_list_api'),
    re_path(r'^buy-subscription/$', BuySubscriptionPlan.as_view(), name='buy_subscription'),
    re_path(r'^my-plans-list/$', MyPurchasedPlansList.as_view(), name='my_plans_list'),
    re_path(r'^view-purchased-plan/$', ViewPurchasedPlan.as_view(), name='view_purchased_plan'),
    re_path(r'^pay-and-renew-plan/$', PayAndRenewPlan.as_view(), name='pay_and_renew_api'),
    
]
