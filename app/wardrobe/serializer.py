from rest_framework.serializers import ModelSerializer
from .models import *
from api.serializer import *

class WardrobeSerializer(ModelSerializer):
    class Meta:
        model = Wardrobe
        fields = ('__all__')
