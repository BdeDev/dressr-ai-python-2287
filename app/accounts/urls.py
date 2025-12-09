from .views import *
from django.contrib import admin
from django.urls import re_path


admin.autodiscover()
app_name = 'accounts'


urlpatterns = [
    
    ## Authentication
    re_path(r'^user-login/$', LoginView.as_view(), name='login'),
    re_path(r'^logout/$', LogOutView.as_view(), name='logout'),
    re_path(r'^reset-password/(?P<uid>[-\w]+)/(?P<token>[-\w]+)/$',ResetPassword.as_view(),name="reset_password_user"),
    re_path(r'^forgot-password-email/$', ForgotPasswordEmail.as_view(), name='forgot_password_email'),

    ## Users
    re_path(r'^change-password/$', PasswordChange.as_view(), name='change_password'),
    re_path(r'^validations/$', Validations, name='validations'),
    
    ## Login History
    re_path(r'^login-history/$', LoginHistoryView.as_view(), name='login_history'),
    re_path(r'^delete-history/$', DeleteHistory.as_view(), name='delete_history'),

    ## Notifications
    re_path(r'^notifications/(?P<id>[-\w]+)/$', NotificationsList.as_view(), name='notifications_list'),
    re_path(r'^delete-notifications/$', DeleteNotifications.as_view(), name='delete_notifications'),
    re_path(r'^mark-read-notifications/(?P<id>[-\w]+)/$', MarkReadNotifications.as_view(), name='mark_read_notifications'),          

    ##Cronjob add
    re_path(r'^list-cronjob/$',ListCronjob.as_view(),name='list_cronjob'),
    re_path(r'^add-cronjob/$',AddCronjob.as_view(),name='add_cronjob'),   
    re_path(r'^remove-cronjob/$',RemoveCronjob.as_view(),name='remove_cronjob'),
    re_path(r'^run-cronjob/(?P<id>[-\w]+)/$',RunCronjob.as_view(),name='run_cronjob'),
    re_path(r'^bulk-notification/$',SendBulkNotification.as_view(),name='bulk_notification'),

    #Django Site Settings
    re_path(r'^update-django-site/$', UpdateDjangoSite.as_view(), name='update_django_site'),

     ## Banners
    re_path(r'^banners-list/$',BannersList.as_view(), name='banners_list'),
    re_path(r'^change-banner-status/(?P<id>[-\w]+)/$',ChangeBannerStatus.as_view(), name='change_banner_status'),
    re_path(r'^delete-banner/(?P<id>[-\w]+)/$',DeleteBanner.as_view(), name='delete_banner'),

]


