from .views import *
from django.contrib import admin
from django.urls import re_path
from .views_api import *

admin.autodiscover()
app_name = 'wardrobe'


urlpatterns = [
    re_path(r'^cloth-category/$', ClothCategoryView.as_view(), name='cloth_category'),
    re_path(r'^delete-cloth-category/(?P<id>[-\w]+)/$', DeleteClothCategory.as_view(), name='delete_cloth_category'),

    re_path(r'^occasion/$', OccasionView.as_view(), name='occasion'),
    re_path(r'^delete-occasion/(?P<id>[-\w]+)/$', DeleteOccasion.as_view(), name='delete_occasion'),

    re_path(r'^accessory/$', AccessoryView.as_view(), name='accessory'),
    re_path(r'^delete-accessory/(?P<id>[-\w]+)/$', DeleteAccessory.as_view(), name='delete_accessory'),


    ### -------------------------------Wardrobe Management--------------------------------
    re_path(r'^add-wardrobe-api/$', AddWardrobe.as_view(), name='add_wardrobe_api'),
    re_path(r'^get-wardrobe-api/$', GetWardrobe.as_view(), name='get_wardrobe_api'),
    re_path(r'^get-all-wardrobe-api/$', GetWardrobs.as_view(), name='get_all_wardrobe_api'),
    re_path(r'^edit-wardrobe-api/$', EditWardrobe.as_view(), name='edir_wardrobe_api'),
    re_path(r'^delete-wardrobe-api/$', DeleteWardrobe.as_view(), name='delete_wardrobe_api'),
    re_path(r'^add-cloth-item-api/$', AddClothItem.as_view(), name='add_cloth_item_api'),
    re_path(r'^edit-cloth-item-api/$', EditWardrobeItem.as_view(), name='edit_cloth_item_api'),
    re_path(r'^remove-cloth-item-api/$', RemoveClothFromWardrobe.as_view(), name='remove_cloth_item_api'),
    re_path(r'^get-cloth-item-api/$', GetClothItem.as_view(), name='get_cloth_item_api'),
    re_path(r'^get-cloths-api/$', GetCloths.as_view(), name='get_cloths_api'),

    # admin panel
    re_path(r'^wardrobe-list/$', WardrobeList.as_view(), name='wardrobe_list'),
    re_path(r'^view-wardrobe/(?P<id>[-\w]+)/$', WardrobeView.as_view(), name='view_wardrobe'),
]