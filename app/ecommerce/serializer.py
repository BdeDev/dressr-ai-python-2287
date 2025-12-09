from rest_framework.serializers import ModelSerializer
from .models import *
from api.serializer import *


class FashionTipSerializer(ModelSerializer):
    class Meta:
        model = FashionTip
        fields = ('__all__')

class BannerSerializer(ModelSerializer):
    class Meta:
        model = Banners
        fields = ('__all__')


class PartnerStoresSerializer(ModelSerializer):
    class Meta:
        model = PartnerStore
        fields = ('__all__')


class RatingSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = ('__all__')