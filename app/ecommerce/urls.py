from .views import *
from django.contrib import admin
from .views_api import *
from django.urls import re_path
from .view_graphs import *
from .view_export import *

admin.autodiscover()
app_name = 'ecommerce'


urlpatterns = [
    ## Fashion Tip Category Management View from admin panel
    re_path(r'^category-list/$', CategoryList.as_view(), name='fashion_category_list'),
    re_path(r'^add-category/$', AddCategory.as_view(), name='add_category'),
    re_path(r'^view-category/(?P<id>[-\w]+)/',ViewCategory.as_view(),name="view_category"),
    re_path(r'^edit-category/(?P<id>[-\w]+)/$',EditCategory.as_view(), name='edit_category'),
    re_path(r'^delete-category/(?P<id>[-\w]+)/$',DeleteCategory.as_view(), name='delete_category'),
    re_path(r'^category-status/(?P<id>[-\w]+)/$',CategoryStatus.as_view(), name='category_status'),

    ## Fashion Tips Management View from admin panel
    re_path(r'^fashion-tip-list/$', FashionTipList.as_view(), name='fashion_tip_list'),
    re_path(r'^add-fashion-tip/$', AddFashionTip.as_view(), name='add_fashion_tip'),
    re_path(r'^view-fashion-tip/(?P<id>[-\w]+)/',ViewFashionTip.as_view(),name="view_fashion_tip"),
    re_path(r'^edit-fashion-tip/(?P<id>[-\w]+)/$',EditFashionTip.as_view(), name='edit_fashion_tip'),
    re_path(r'^delete-fashion-tip/(?P<id>[-\w]+)/$',DeleteFashionTip.as_view(), name='delete_fashion_tip'),
    re_path(r'^fashion-tip-status/(?P<id>[-\w]+)/$',PublishUnpublishFashionTip.as_view(), name='publish_unpublish_fashion_tip'),

    # Partner Store View from admin panel
    re_path(r'^partner-store/$', PartnerStoreView.as_view(), name='partner_store'),
    re_path(r'^delete-store/(?P<id>[-\w]+)/$', DeletePartnerStore.as_view(), name='delete_store'),

    ## Discount Ads Management View from admin panel
    re_path(r'^discount-list/$', DiscountAdsList.as_view(), name='discount_list'),
    re_path(r'^add-discount/$', AddDiscountAd.as_view(), name='add_discount'),
    re_path(r'^view-discount/(?P<id>[-\w]+)/',ViewDiscountAd.as_view(),name="view_discount"),
    re_path(r'^edit-discount/(?P<id>[-\w]+)/$',EditDiscountAd.as_view(), name='edit_discount'),
    re_path(r'^delete-discount/(?P<id>[-\w]+)/$',DeleteDiscountAd.as_view(), name='delete_discount'),
    re_path(r'^discount-status/(?P<id>[-\w]+)/$',PublishUnpublishDiscountAd.as_view(), name='publish_unpublish_discount'),

    ###### api management
    re_path(r'^banners-list-api/$', BannersListAPI.as_view(), name='banner_list_api'),
    re_path(r'^fashion-tips-list-api/$', FashionTipsAPI.as_view(), name='fashion_tips_list_api'),
    re_path(r'^partner-store-api/$', PartnerStoresAPI.as_view(), name='partner_store_api'),

    re_path(r'^affiliate-graph/$', AffiliateGraph.as_view(), name='affiliate_graph'),
    re_path(r'^affiliate-performance-graph/$', AffiliatePerformanceGraph.as_view(), name='affiliate_performance_graph'),
    re_path(r'^download-performance-report/$', DownloadAffiliatePerformanceReport.as_view(), name='download_performance_report'),


    # Feedback api
    re_path(r'^add-feedback-api/$', AddRatingAPI.as_view(), name='add_feedback_api'),
  

    # Feedback Management on admin panel
    re_path(r'^feedback-list/(?P<id>[-\w]+)/$', UserFeedBackList.as_view(), name='feedback_list'),

    # Virtual try on Management on admin panel
    re_path(r'^virtual-try-on-list/$', VirtualTryOnList.as_view(), name='virtual_try_on_list'),
    re_path(r'^view-virtual-try-on/(?P<id>[-\w]+)/$', ViewTryOnDetails.as_view(), name='view_virtual_try_on'),
    re_path(r'^delete-virtual-try-on/(?P<id>[-\w]+)/$', DeleteVirtualTryOn.as_view(), name='delete_virtual_try_on'),
    re_path(r'^sync-virtual-try-on-data/$', SyncTryOnData.as_view(), name='sync_virtual_try_on_data'),
   
]