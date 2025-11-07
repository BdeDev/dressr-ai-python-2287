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


    ### -------------------------------Wardrobe Management--------------------------------###
    re_path(r'^get-wardrobe-api/$', GetWardrobeAPI.as_view(), name='get_wardrobe_api'),
    re_path(r'^edit-wardrobe-api/$', EditWardrobeAPI.as_view(), name='edit_wardrobe_api'),
    re_path(r'^add-item-api/$', AddItemInWardrobeAPI.as_view(), name='add_item_api'),
    re_path(r'^edit-wardrobe-item-api/$', EditWardrobeItemAPI.as_view(), name='edit_wardrobe_item_api'),
    re_path(r'^remove-item-api/$', RemoveItemFromWardrobeAPI.as_view(), name='remove_item_api'),
    re_path(r'^get-item-api/$', GetItemAPI.as_view(), name='get_item_api'),
    re_path(r'^get-items-api/$', GetItemsAPI.as_view(), name='get_items_api'),

    ###--------------------------------Wardrobe essentials--------------------------####
    re_path(r'^accessories-api/$', GetAccessoriesAPI.as_view(), name='accessories_api'),
    re_path(r'^occasions-api/$', GetOccasionsAPI.as_view(), name='occasions_api'),
    re_path(r'^category-listing-api/$', GetClothCategoriesAPI.as_view(), name='categories_api'),

    ###-----------------------------OutFit Management------------------------------####
    re_path(r'^create-outfit-api/$', CreateOutfitAPI.as_view(), name='create_outfit_api'),
    re_path(r'^my-outfit-list-api/$', MyOutFitListAPI.as_view(), name='my_outfit_list_api'),
    re_path(r'^get-my-outfit-api/$', GetMyOutfitAPI.as_view(), name='get_my_outfit_api'),
    re_path(r'^delete-my-outfit-api/$', DeleteOutfitAPI.as_view(), name='delete_my_outfit_api'),
    re_path(r'^delete-item-from-my-outfit-api/$', RemoveItemsFromOutfitAPI.as_view(), name='delete_item_drom_my_outfit_api'),
    re_path(r'^add-item-in-my-outfit-api/$', AddItemInOutfitAPI.as_view(), name='add_item_in_outfit_api'),


    ###--------------------------------Wardrobe essentials-----------------------####
    re_path(r'^accessories-api/$', GetAccessoriesAPI.as_view(), name='accessories_api'),
    re_path(r'^occasions-api/$', GetOccasionsAPI.as_view(), name='occasions_api'),
    re_path(r'^cloth-category-listing-api/$', GetClothCategoriesAPI.as_view(), name='clothcategories_api'),



    ###-----------------------------OutFit Management-----------------------####
    re_path(r'^create-outfit-api/$', CreateOutFitAPI.as_view(), name='create_outfit_api'),
    re_path(r'^my-outfit-list-api/$', MyOutFitListAPI.as_view(), name='my_outfit_list_api'),

    # admin panel
    re_path(r'^wardrobe-list/$', WardrobeList.as_view(), name='wardrobe_list'),
    re_path(r'^view-wardrobe/(?P<id>[-\w]+)/$', WardrobeView.as_view(), name='view_wardrobe'),
]