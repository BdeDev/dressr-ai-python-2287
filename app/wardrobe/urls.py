from .views import *
from django.contrib import admin
from django.urls import re_path

admin.autodiscover()
app_name = 'wardrobe'


urlpatterns = [
    re_path(r'^cloth-category/$', ClothCategoryView.as_view(), name='cloth_category'),
    re_path(r'^delete-cloth-category/(?P<id>[-\w]+)/$', DeleteClothCategory.as_view(), name='delete_cloth_category'),

    re_path(r'^occasion/$', OccasionView.as_view(), name='occasion'),
    re_path(r'^delete-occasion/(?P<id>[-\w]+)/$', DeleteOccasion.as_view(), name='delete_occasion'),

    re_path(r'^accessory/$', AccessoryView.as_view(), name='accessory'),
    re_path(r'^delete-accessory/(?P<id>[-\w]+)/$', DeleteAccessory.as_view(), name='delete_accessory'),
]