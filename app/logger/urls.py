from django.contrib import admin
from .views import *
from django.urls import re_path


admin.autodiscover()
app_name = 'logger'


urlpatterns = [

    ## Error Logs
    re_path(r'^error-logs/$',ErrorLogsList.as_view(),name="error_logs_list"),
    re_path(r'^delete-all-logs/$',DeleteAllLogs.as_view(),name="delete_all_logs"),
    re_path(r'^delete-error-log/(?P<id>[-\w]+)/$',DeleteErrorLog.as_view(),name="delete_error_log"),
    re_path(r'^view-error-log/(?P<id>[-\w]+)/$',ViewErrorLog.as_view(),name="view_error_log"),

    ## Email Logger
    re_path(r'^email-logs/$',EmailLogsList.as_view(),name="email_logs_list"),
    re_path(r'^email-logs-delete/$',DeleteEmailLogs.as_view(),name="delete_email_logs"),
    re_path(r'^view-email-log/(?P<id>[-\w]+)/$',ViewEmailLog.as_view(),name="view_email_log"),
    re_path(r'^delete-email-log/(?P<id>[-\w]+)/$',DeleteEmailLog.as_view(),name="delete_email_log"),
    re_path(r'^resend-email/(?P<id>[-\w]+)/$',ResendEmail.as_view(),name="resend_email"),
    re_path(r'^send-custom-email/(?P<id>[-\w]+)/$',SendCustomEmail.as_view(),name="send_custom_email"),

    ## Application Crash Logs
    re_path(r'crash-logs/$',CrashLogs.as_view(),name="crash_logs"),
    re_path(r'crash-logs-delete/$',DeleteAllCrashLogs.as_view(),name="delete_all_crash_logs"),
    re_path(r'delete-crash-log/(?P<id>[-\w]+)/$',DeleteCrashLog.as_view(),name="delete_crash_log"),
    re_path(r'view-crash-log/(?P<id>[-\w]+)/$',ViewCrashLog.as_view(),name="view_crash_log"),
    
    ## Application Crash Logs API
    re_path(r'create-crash-log/$',CreateCrashLog.as_view(),name="create_crash_log"),
    re_path(r'get-crash-log/$',GetCrashLog.as_view(),name="get_crash_log"),

    ## Email campaigns
    re_path(r'^campaign-templates/$',CampaignTemplateList.as_view(),name="campaign_templates"),
    re_path(r'^save-campaign-template/$',SaveCampaignTemplate.as_view(),name="save_campaign_template"),
    re_path(r'^delete-campaign-template-draft/(?P<id>[-\w]+)/$',DeleteCampaignTemplate.as_view(),name="delete_campaign_template"),
    re_path(r'^send-campaign-email/(?P<id>[-\w]+)/$',SendCampaignEmails.as_view(),name="send_campaign_email"),

    ## SMS campaigns
    re_path(r'^sms-campaign-templates/$',SMSCampaignTemplateList.as_view(),name="sms_campaign_templates"),
    re_path(r'^save-sms-campaign-template/$',SaveSMSCampaignTemplate.as_view(),name="save_sms_campaign_template"),
    re_path(r'^delete-sms-campaign-template-draft/(?P<id>[-\w]+)/$',DeleteSMSCampaignTemplate.as_view(),name="delete_sms_campaign_template"),
    re_path(r'^send-campaign-sms/(?P<id>[-\w]+)/$',SendCampaignSMS.as_view(),name="send_campaign_sms"),
    
]
