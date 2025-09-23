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
    re_path(r'^edit-admin/(?P<id>[-\w]+)/$',EditAdmin.as_view(), name='edit_admin'),
    re_path(r'^users-list/$', UsersList.as_view(), name='users_list'),
    re_path(r'^add-user/$', AddUser.as_view(), name='add_user'),
    re_path(r'^edit-user/(?P<id>[-\w]+)/$', EditUser.as_view(), name='edit_user'),
    
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
]