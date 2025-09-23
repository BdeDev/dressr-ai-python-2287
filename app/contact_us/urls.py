from django.contrib import admin
from .views import *
from django.urls import re_path


admin.autodiscover()
app_name = 'contact_us'


urlpatterns = [
    ## Contact Us
    re_path(r'contact-us-list/$',ContactUsList.as_view(),name="contactus_list"),
    re_path(r'view-contact-us-details/(?P<id>[-\w]+)/$',ViewContactUsDetails.as_view(),name="view_contact"),
    re_path(r'delete-contact-us/(?P<id>[-\w]+)/$',DeleteContactUs.as_view(),name="delete_contact"),
    re_path(r'contactus-reply/$',ContactUsReplyView.as_view(),name="contactus_reply"),

    ## Social Links Management
    re_path(r'social-links/$',SocialLinksView.as_view(),name="social_links"),
]
