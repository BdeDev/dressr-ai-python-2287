from rest_framework.serializers import ModelSerializer
from .models import *
from accounts.utils import *
from api.serializer import *

class ClothItemSerializer(ModelSerializer):
    cloth_category = SerializerMethodField()
    is_favourite = SerializerMethodField()
    
    class Meta:
        model = ClothingItem
        fields = ['id','title','wardrobe','image','cloth_category','occasion',
                  'accessory','weather_type','color','price','brand','date_added','last_worn','wear_count','item_url','tags','is_favourite']

    def get_cloth_category(self,obj):
        return obj.cloth_category.id,obj.cloth_category.title
    
    def get_is_favourite(self, obj):
        user = self.context.get("request").user
        return 1 if obj.favourite.filter(id=user.id).exists() else 0


class WardrobeSerializer(ModelSerializer):
    cloth_items = SerializerMethodField(read_only=True)
    class Meta:
        model = Wardrobe
        fields = ('__all__')

    def get_cloth_items(self,obj):
        request = self.context.get('request')
        cloth_objects = ClothingItem.objects.filter(wardrobe = obj)
        if cloth_objects: 
            start,end,meta_data = get_pages_data(request.query_params.get('page', None), cloth_objects)
            data = ClothItemSerializer(cloth_objects[start : end],many=True , context={"request": request}).data
            return data
        else:
            return None
        

class AccessorySerializer(ModelSerializer):
    class Meta:
        model = Accessory
        fields = ('__all__')


class OccasionSerializer(ModelSerializer):
    class Meta:
        model = Occasion
        fields = ('__all__')

class ClothCategorySerializer(ModelSerializer):
    class Meta:
        model = ClothCategory
        fields = ('__all__')

class MyOutFitSerializer(ModelSerializer):
    items = SerializerMethodField(read_only=True)
    is_favourite = SerializerMethodField()

    class Meta:
        model = Outfit
        fields = ['id','title','items','occasion','weather_type','created_by','color','notes','image','is_favourite']

    def get_items(self, obj):
        items = obj.items.all()
        return [
            {
                "id": item.id,
                "title": item.title,
                "image": self.context.get('request').build_absolute_uri(item.image.url) if USE_HTTPS else self.context.get('request').build_absolute_uri(item.image.url),
                "category_title": item.cloth_category.title
            }
            for item in items
        ]

    def get_image(self,obj):
        return  self.context.get('request').build_absolute_uri(obj.image.url) if USE_HTTPS else self.context.get('request').build_absolute_uri(obj.image.url),

    def get_is_favourite(self, obj):
        user = self.context.get("request").user
        return 1 if obj.favourite.filter(id=user.id).exists() else 0

class TripsSerializer(ModelSerializer):
    outfit = SerializerMethodField()
    activity_flag = SerializerMethodField()

    class Meta:
        model = Trips
        fields = '__all__'

    def get_outfit(self, obj):
        request = self.context.get("request")

        return [
            {
                "id": trip_outfit.id,
                "title": trip_outfit.title,
                "image": request.build_absolute_uri(trip_outfit.image.url) if trip_outfit.image else None
            }
            for trip_outfit in obj.outfit.all()
        ]

    def get_activity_flag(self,obj):

        return [
            {
                "id": flag.id,
                "name": flag.name,
                "description": flag.description,
            }
            for flag in obj.activity_flag.all()
        ]


class ActivityFlagSerializer(ModelSerializer):
    class Meta:
        model = ActivityFlag
        fields = ('__all__')

class WearHistorySerializer(ModelSerializer):
    item = SerializerMethodField(read_only=True)
    class Meta:
        model = WearHistory
        fields = ('__all__')

    def get_item(self, obj):
        request = self.context.get("request")
        return {
                "id": obj.item.id,
                "title": obj.item.title,
                "image": request.build_absolute_uri(obj.item.image.url) if USE_HTTPS else request.build_absolute_uri(obj.item.image.url),
                "category_title": obj.item.cloth_category.title,
                "brand":obj.item.brand
            }


class RecentSearchSerializer(ModelSerializer):
    class Meta:
        model = RecentSearch
        fields = ('__all__')


class ItemUsageFrequencySerializer(ModelSerializer):
    is_favourite = SerializerMethodField()

    class Meta:
        model = ClothingItem
        fields = ['id','title','wardrobe','image','cloth_category','occasion',
                  'accessory','weather_type','color','price','brand','date_added','last_worn','wear_count','item_url','tags','is_favourite']

    def get_image(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.image.url) if USE_HTTPS else request.build_absolute_uri(obj.image.url),

    def get_is_favourite(self, obj):
        user = self.context.get("request").user
        return 1 if obj.favourite.filter(id=user.id).exists() else 0