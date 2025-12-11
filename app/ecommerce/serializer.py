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
    user = SerializerMethodField()
    class Meta:
        model = Rating
        fields = ('__all__')

class RatingSerializer(ModelSerializer):
    user = SerializerMethodField()

    class Meta:
        model = Rating
        fields = "__all__"

    def get_user(self, obj):
        request = self.context.get("request")
        
        if obj.user.profile_pic:
            url = request.build_absolute_uri(obj.user.profile_pic.url) if obj.user.profile_pic.url else ''
        else:
            url = ""

        user_data = {
            "id": obj.user.id,
            "full_name": obj.user.full_name,
            "profile_pic": url,
        }
        return user_data
