from rest_framework.serializers import ModelSerializer
from .models import *
from api.serializer import *



class ClothItemSerializer(ModelSerializer):
    class Meta:
        model = ClothingItem
        fields = ('__all__')


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