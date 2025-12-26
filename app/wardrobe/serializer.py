from rest_framework.serializers import ModelSerializer
from .models import *
from accounts.utils import *
from api.serializer import *
from ecommerce.serializer import RatingSerializer

class ClothItemSerializer(ModelSerializer):
    cloth_category = SerializerMethodField()
    is_favourite = SerializerMethodField()
    feedback = SerializerMethodField()
    thumbnail = SerializerMethodField()
    image = SerializerMethodField()
    
    class Meta:
        model = ClothingItem
        fields = ['id','title','wardrobe','image','cloth_category','occasion','thumbnail',
                  'accessory','weather_type','color','price','brand','date_added','last_worn','wear_count','item_url','is_favourite','feedback']

    def get_cloth_category(self, obj):
        return (
            obj.cloth_category.id,
            obj.cloth_category.title
        ) if obj.cloth_category else None
    
    def get_is_favourite(self, obj):
        user = self.context.get("request").user
        return 1 if obj.favourite.filter(id=user.id).exists() else 0

    def get_feedback(self, obj):
        feedback = obj.rating_set.all()
        if not feedback.exists():
            return None
        return RatingSerializer(feedback, many=True,context=self.context).data
    
    def get_thumbnail(self, obj):
        try:
            url=self.context.get('request').build_absolute_uri(obj.thumbnail.url)  
            if url:
                url=url.split('://')[1]
            return  'https://'+url if USE_HTTPS else 'http://' + url 
        except:
            return None
        

    def get_image(self, obj):
        try:
            url=self.context.get('request').build_absolute_uri(obj.image.url)  
            if url:
                url=url.split('://')[1]
            return  'https://'+url if USE_HTTPS else 'http://' + url 
        except:
            return None


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
    feedback = SerializerMethodField()
    image = SerializerMethodField()

    class Meta:
        model = Outfit
        fields = ['id','title','items','occasion','weather_type','created_by','color','notes','image','is_favourite','feedback']

    def get_items(self, obj):
        request = self.context.get('request')
        items = obj.items.select_related('cloth_category')

        result = []

        for item in items:
            image = None
            if item.image:
                url = request.build_absolute_uri(item.image.url)
                url = url.split('://')[1]
                image = 'https://'+url if USE_HTTPS else 'http://' + url 

            result.append({
                "id": item.id,
                "title": item.title,
                "image": image,
                "category_title": item.cloth_category.title if item.cloth_category else None
            })

        return result

    def get_image(self,obj):
        try:
            url=self.context.get('request').build_absolute_uri(obj.image.url)  
            if url:
                url=url.split('://')[1]
            return  'https://'+url if USE_HTTPS else 'http://' + url 
        except:
            return None
      

    def get_is_favourite(self, obj):
        user = self.context.get("request").user
        return 1 if obj.favourite.filter(id=user.id).exists() else 0
    
    def get_feedback(self, obj):
        feedback = obj.rating_set.all()
        if not feedback.exists():
            return None
        return RatingSerializer(feedback, many=True,context=self.context).data

class TripsSerializer(ModelSerializer):
    outfit = SerializerMethodField()
    activity_flag = SerializerMethodField()

    class Meta:
        model = Trips
        fields = '__all__'


    def get_outfit(self, obj):
        request = self.context.get("request")
        result = []
        for trip_outfit in obj.outfit.all():
            image = None
            if trip_outfit.image:
                url = request.build_absolute_uri(trip_outfit.image.url)
                url = url.split('://')[1]
                image = 'https://'+url if USE_HTTPS else 'http://' + url 

            result.append({
                "id": trip_outfit.id,
                "title": trip_outfit.title,
                "image": image
            })

        return result


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
        url=self.context.get('request').build_absolute_uri(obj.item.image.url)  
        if url:
            url=url.split('://')[1]
        image = 'https://'+url if USE_HTTPS else 'http://' + url 

        return {
                "id": obj.item.id,
                "title": obj.item.title,
                "image": image,
                "category_title": obj.item.cloth_category.title if obj.item.cloth_category else None ,
                "brand":obj.item.brand
            }


class RecentSearchSerializer(ModelSerializer):
    class Meta:
        model = RecentSearch
        fields = ('__all__')


class ItemUsageFrequencySerializer(ModelSerializer):
    is_favourite = SerializerMethodField()
    image = SerializerMethodField()

    class Meta:
        model = ClothingItem
        fields = ['id','title','wardrobe','image','cloth_category','occasion', 'accessory','weather_type','color','price','brand','date_added','last_worn','wear_count','item_url','is_favourite']

    def get_image(self, obj):
        try:
            url=self.context.get('request').build_absolute_uri(obj.image.url)  
            if url:
                url=url.split('://')[1]
            return  'https://'+url if USE_HTTPS else 'http://' + url 
        except:
            return None

    def get_is_favourite(self, obj):
        user = self.context.get("request").user
        return 1 if obj.favourite.filter(id=user.id).exists() else 0


class OutfitSiggestionSerializer(ModelSerializer):
    items = SerializerMethodField()
    is_favourite = SerializerMethodField()
    
    class Meta:
        model = OutfitSiggestion
        fields = ['id','occasion','explanation','today_outfit','items','is_favourite']

    def get_items(self, obj):
        request = self.context.get('request')
        use_https = True

        result = []
        for item in obj.items.all():
            if item.image:
                url = request.build_absolute_uri(item.image.url)
                if url:
                    url = url.split('://')[1]
                image = 'https://' + url if use_https else 'http://' + url
            else:
                image = None

            result.append({
                "id": item.id,
                "title": item.title,
                "image": image,
                "category_title": item.cloth_category.title if item.cloth_category else None,
                "brand": item.brand
            })
        return result
    
    def get_is_favourite(self, obj):
        user = self.context.get("request").user
        return 1 if obj.favourite.filter(id=user.id).exists() else 0