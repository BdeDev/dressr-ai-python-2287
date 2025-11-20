from rest_framework.serializers import ModelSerializer
from .models import *
from accounts.utils import *
from api.serializer import *

class ClothItemSerializer(ModelSerializer):
    cloth_category = SerializerMethodField()
    
    class Meta:
        model = ClothingItem
        fields = ('__all__')

    def get_cloth_category(self,obj):
        return obj.cloth_category.id,obj.cloth_category.title


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

    class Meta:
        model = Outfit
        fields = ('__all__')

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

class TripsSerializer(ModelSerializer):
    class Meta:
        model = Trips
        fields = ('__all__')


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

        return {
                "id": obj.item.id,
                "title": obj.item.title,
                "image": self.context.get('request').build_absolute_uri(obj.item.image.url) if USE_HTTPS else self.context.get('request').build_absolute_uri(obj.item.image.url),
                "category_title": obj.item.cloth_category.title,
                "brand":obj.item.brand
            }
           
        

class RecentSearchSerializer(ModelSerializer):
    class Meta:
        model = RecentSearch
        fields = ('__all__')


class ItemUsageFrequencySerializer(ModelSerializer):
    class Meta:
        model = ClothingItem
        fields = ['id', 'title', 'image', 'wear_count']