from rest_framework.serializers import ModelSerializer
from .models import *
from api.serializer import *


class FashionTipSerializer(ModelSerializer):
    class Meta:
        model = FashionTip
        fields = ('__all__')