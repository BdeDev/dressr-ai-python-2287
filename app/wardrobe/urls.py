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

    re_path(r'^sync-default-hair-color/$', SyncDefaultHairColor.as_view(), name='sync_default_hair_color'),
    re_path(r'^sync-default-skin-tone/$', SyncDefaultSkinTone.as_view(), name='sync_default_skin_tone'),
    re_path(r'^hair-color-list/$', HairColorList.as_view(), name='hair_color_list'),
    re_path(r'^skin-tone-list/$', SkinToneList.as_view(), name='skin_tone_list'),
    re_path(r'^sync-default-body-type/$', SyncDefaultBodyType.as_view(), name='sync_default_body_type'),
    re_path(r'^body-type-list/$', BodyTypeList.as_view(), name='body_type_list'),
    re_path(r'^delete-body-type/(?P<id>[-\w]+)/$', DeleteBodyType.as_view(), name='delete_body_type'),
    re_path(r'^delete-hair-color/(?P<id>[-\w]+)/$', DeleteHairColor.as_view(), name='delete_hair_color'),
    re_path(r'^delete-skin-tone/(?P<id>[-\w]+)/$', DeleteSkinTone.as_view(), name='delete_skin_tone'),


    re_path(r'^activity-flags/$', ActivityFlags.as_view(), name='activity_flags'),
    re_path(r'^delete-activity-flag/(?P<id>[-\w]+)/$', DeleteActivityFlag.as_view(), name='delete_activity_flag'),
    re_path(r'^sync-default-activity-flag/$', SyncDefaultActivityFlag.as_view(), name='sync_default_activity_flag'),

    re_path(r'^user-trip-list/$', UserTrips.as_view(), name='trip_list'),
    re_path(r'^view-trip-details/(?P<id>[-\w]+)/$', ViewTripDetails.as_view(), name='view_trip_detail'),
    re_path(r'^user-outfit-list/$', UserOutfit.as_view(), name='user_outfit_list'),
    re_path(r'^view-outfit-details/(?P<id>[-\w]+)/$', ViewOutfitDetails.as_view(), name='view_outfit_detail'),

    ### -------------------------------Wardrobe Management--------------------------------###
    re_path(r'^get-wardrobe-api/$', GetWardrobeAPI.as_view(), name='get_wardrobe_api'),
    re_path(r'^edit-wardrobe-api/$', EditWardrobeAPI.as_view(), name='edit_wardrobe_api'),
    re_path(r'^add-item-api/$', AddItemInWardrobeAPI.as_view(), name='add_item_api'),
    re_path(r'^edit-wardrobe-item-api/$', EditWardrobeItemAPI.as_view(), name='edit_wardrobe_item_api'),
    re_path(r'^remove-item-api/$', RemoveItemFromWardrobeAPI.as_view(), name='remove_item_api'),
    re_path(r'^remove-all-items-api/$', RemoveAllItemFromWardrobeAPI.as_view(), name='remove_all_items_api'),
    re_path(r'^get-item-api/$', GetItemAPI.as_view(), name='get_item_api'),
    re_path(r'^get-items-api/$', GetItemsAPI.as_view(), name='get_items_api'),
    re_path(r'^marked-favourite-item-api/$', MarkItemFavouriteAPI.as_view(), name='mark_favourite_item_api'),
    re_path(r'^get-cloth-item-by-category-api/$', GetItemByCategoryAPI.as_view(), name='get_cloth_item_by_category_api'),
    re_path(r'^add-multiple-item-api/$', AddMultipleItemInWardrobeAPI.as_view(), name='add_multiple_item_api'),
    re_path(r'^favourite-item-list-api/$', FavouriteItemListAPI.as_view(), name='favourite_item_list_api'),


    re_path(r'^item-search-api/$', ItemSeachFilterAPI.as_view(), name='item_search_api'),
    re_path(r'^recent-search-api/$', RecentSearchAPI.as_view(), name='recent_search_api'),
    re_path(r'^remove-item-from-recent-search-api/$', RemoveItemFromRecentSearchAPI.as_view(), name='remove_item_fron_recent_search_api'),
    re_path(r'^remove-all-recent-search-api/$', RemoveAllItemFromRecentSearchAPI.as_view(), name='remove_all_recent_search_api'),

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
    re_path(r'^marked-favourite-outfit-api/$', MarkOutfitFavouriteAPI.as_view(), name='mark_favourite_outfit_api'),
    re_path(r'^favourite-outfit-list-api/$', FavouriteOutfitListAPI.as_view(), name='favourite_outfit_list_api'),

    ##--------------------------------Trip Management-------------------------------##
    re_path(r'^add-activity-flag-api/$', AddAcivityFlagsAPI.as_view(), name='add_activity_flag_api'),
    re_path(r'^edit-activity-flag-api/$', EditAcivityFlagsAPI.as_view(), name='edit_activity_flag_api'),
    re_path(r'^activity-flag-list-api/$', ActivityFlagListAPI.as_view(), name='activity_flag_list_api'),
    re_path(r'^my-activity-flag-list-api/$', MyActivityFlagListAPI.as_view(), name='my_activity_flag_list_api'),
    re_path(r'^delete-my-activity-flag-api/$', DeleteMyActivityFlagAPI.as_view(), name='delete_my_activity_flag_api'),

    re_path(r'^add-trip-api/$', AddTripAPI.as_view(), name='add_trip_api'),
    re_path(r'^item-recommendation-for-trip-api/$', OutfitRecommendationAPI.as_view(), name='item_recommendation_for_trip_api'),
    re_path(r'^get-trip-list-api/$', GetMyAllTripAPI.as_view(), name='get_trip_list_api'),
    re_path(r'^get-trip-api/$', GetMyTripOutfitsAPI.as_view(), name='get_trip_api'),
    re_path(r'^delete-trip-api/$', DeleteTripAPI.as_view(), name='delete_trip_api'),

    ##-----------------------------------admin panel----------------------------------
    re_path(r'^wardrobe-list/$', WardrobeList.as_view(), name='wardrobe_list'),
    re_path(r'^view-wardrobe/(?P<id>[-\w]+)/$', WardrobeView.as_view(), name='view_wardrobe'),
    re_path(r'^view-item-details/(?P<id>[-\w]+)/$', ViewItemDetails.as_view(), name='view_item_detais'),
    re_path(r'^item-details-ajax/$', WardrobeItemsDetails.as_view(), name='wardrobe_item_details'),
    
    ##-----------------------------------Item Wear Logs----------------------------########
    re_path(r'^wear-log-api/$', WearLogAPI.as_view(), name='wear_log_api'),
    re_path(r'^wear-calendar-api/$', WearCalendarAPI.as_view(), name='wear_calendar_api'),
    re_path(r'^get-wear-log-history-api/$', GetWearLogsByItemAPI.as_view(), name='get_wear_log_history_api'),
    re_path(r'^wardrobe-analytics-api/$', MostWearClothAnalyticsAPI.as_view(), name='wardrobe_analytics_api'),

    re_path(r'^view-item-wear-calender/(?P<id>[-\w]+)/$', ViewItemWearCalender.as_view(), name='view_item_wear_calender'),
    re_path(r'^calendar-data-ajax/$', CalenderDataAjax.as_view(), name='calender_data_ajax'),

]