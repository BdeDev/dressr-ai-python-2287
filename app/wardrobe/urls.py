from .views import *
from django.contrib import admin
from django.urls import re_path

admin.autodiscover()
app_name = 'wardrobe'


urlpatterns = []