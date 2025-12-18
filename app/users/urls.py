from .views import *
from django.contrib import admin
from django.urls import re_path
from .views_graphs import *
from .views_exports import *

admin.autodiscover()
app_name = 'users'

urlpatterns = [
    ## Users
    re_path(r'^view-profile/(?P<id>[-\w]+)/$',ViewUser.as_view(), name='view_user'),
    re_path(r'^delete-users/(?P<id>[-\w]+)/$',DeleteUsers.as_view(), name='delete_users'),
    re_path(r'^edit-admin/(?P<id>[-\w]+)/$',EditAdmin.as_view(), name='edit_admin'),
    re_path(r'^users-list/$', UsersList.as_view(), name='users_list'),
    re_path(r'^modify-customer-stripe-account/(?P<id>[-\w]+)/$', ModifyCustomerStipeAccount.as_view(), name='modify_customer_stripe_account'),

    ## User Actions
    re_path(r'^deactivate-user/(?P<id>[-\w]+)/$',InactivateUser.as_view(), name='inactivate_user'),
    re_path(r'^delete-user/(?P<id>[-\w]+)/$',DeleteUser.as_view(), name='delete_user'),
    re_path(r'^activate-user/(?P<id>[-\w]+)/$',ActivateUser.as_view(), name='activate_user'),

    ## Notification Actions
    re_path(r'^notification-on-off/(?P<id>[-\w]+)/$', NotificationOnOff.as_view(), name='notification_on_off'),
    re_path(r'^email-notification-on-off/(?P<id>[-\w]+)/$', EmailNotificationOnOff.as_view(), name='email_notification_on_off'),

    ## Panel Graphs
    re_path(r'^user-graph/$', UserGraph.as_view(), name='users_graph'),
    
    ## Download User Reports
    re_path(r'^download-customer-reports/$',DownLoadCustomerReports.as_view(), name='download_customer_reports'),

    ## Affiiate Management from admin panel
    re_path(r'^affiliate-list/$', AffiliateList.as_view(), name='affiliate_list'),
    re_path(r'^add-affiliate/$', AddAffiliate.as_view(), name='add_affiliate'),
    re_path(r'^edit-affiliate/(?P<id>[-\w]+)/$', EditAffiliate.as_view(), name='edit_affiliate'),
    re_path(r'^edit-affiliate-commission/(?P<id>[-\w]+)/$', UpdateAffiliateCommission.as_view(), name='edit_affiliate_commission'),
]