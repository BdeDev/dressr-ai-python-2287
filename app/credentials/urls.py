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

    ##Firebase Credentials
    re_path(r'^firebase-credentials-list/$',FirebaseKeysList.as_view(),name="firebase_credentials_list"),
    re_path(r'^view-firebase-credentials/(?P<id>[-\w]+)/$',ViewFirebaseKeys.as_view(),name="view_firebase_credentials"),
    re_path(r'^change-firebase-status/(?P<id>[-\w]+)/$',ActivateFirebaseStatus.as_view(),name="change_firebase_status"),
    re_path(r'^update-firebase-credentials/$',UpdateFirebaseKeys.as_view(),name="update_firebase_credentials"),
    re_path(r'^delete-firebase-credentials/(?P<id>[-\w]+)/$',DeleteFirebase.as_view(),name="delete_firebase_credentials"),

    # #Stripe Keys
    re_path(r'^stripe-keys/$',StripeSettingList.as_view(),name="stripe_keys"),
    re_path(r'^edit-stripe-keys/$',EditStripeSetting.as_view(),name="edit_stripe_keys"),
    re_path(r'^view-stripe-keys/(?P<id>[-\w]+)/$',ViewStripeSetting.as_view(),name="view_stripe_keys"),
    re_path(r'^delete-stripe-keys/(?P<id>[-\w]+)/$',DeleteStripeSetting.as_view(),name="delete_stripe_keys"),
    re_path(r'^change-stripe-keys/(?P<id>[-\w]+)/$',ChangeStripeStatus.as_view(),name="change_stripe_keys"),


    ##LightX Editor API Key
    re_path(r'^lightx-editor-key-list/$',LightXEditorCredsList.as_view(),name="lightx_editor_key_list"),
    re_path(r'^delete-lightx-editor-key/(?P<id>[-\w]+)/$',DeleteLightXEditorCredentials.as_view(),name="delete_lightx_creds"),
    re_path(r'^change-lightx-editor-key-status/(?P<id>[-\w]+)/$',ChangeLightXEditorCredsStatus.as_view(),name="change_lightx_key_status"),

]
