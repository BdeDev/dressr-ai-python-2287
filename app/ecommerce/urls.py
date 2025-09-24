from .views import *
from django.contrib import admin
from .views import *
from django.urls import re_path

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

]