from rest_framework.serializers import ModelSerializer
from subscription.models import *
from api.serializer import *


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = SubscriptionPlans
        fields = ('__all__')


class PurchasedPlanListingSerializer(ModelSerializer):
    purchased_by=MinorUserSerializer()

    class Meta:
        model = UserPlanPurchased
        exclude = ('subscription_plan','invoice','activated_on','expire_on','updated_on')

class PurchasedPlanSerializer(ModelSerializer):
    purchased_by=MinorUserSerializer()

    class Meta:
        model = UserPlanPurchased
        exclude = ('subscription_plan',)
