from .views import *
from django.contrib import admin
from django.urls import re_path
admin.autodiscover()
app_name = 'credentials'

urlpatterns = [
    ## SMTP Settings
    re_path(r'^smtp-list/$',SMTPListView.as_view(),name="smtp_list"),
    re_path(r'^add-smtp/$',AddSMTPView.as_view(),name="add_smtp"),
    re_path(r'^delete-smtp/(?P<id>[-\w]+)/$', DeleteSMTP.as_view(), name='delete_smtp'),
    re_path(r'^view-smtp/(?P<id>[-\w]+)/$', ViewSMTP.as_view(), name='view_smtp'),
    re_path(r'^edit-smtp/(?P<id>[-\w]+)/$', EditSMTP.as_view(), name='edit_smtp'),
    re_path(r'^active-deactive-smtp/(?P<id>[-\w]+)/$', ActivateDeActiveSMTP.as_view(), name='active_deactive_smtp'),

    ## Customer Prompt
    re_path(r'^smtp-prompt/$',SMTPPrompt.as_view(),name="smtp_prompt"),
]
