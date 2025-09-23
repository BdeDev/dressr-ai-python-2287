from rest_framework.serializers import ModelSerializer
from .models import *


class ApplicationCrashLogsSerializer(ModelSerializer):
    class Meta:
        model=ApplicationCrashLogs
        fields="__all__"
