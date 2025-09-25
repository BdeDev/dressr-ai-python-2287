from django.db import models
from accounts.common_imports import *
from accounts.models import *
from accounts.constants import *
from subscription.models import *


class ProductCategory(CommonInfo):
    """
    Categories like Shirts, Jeans, Dresses, Accessories
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'product_category'


class Product(CommonInfo):
    """
    Products managed by admin for virtual try-ons
    """
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True, related_name="products")
    name = models.CharField(max_length=150,blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    size = models.CharField(max_length=50, blank=True, null=True)
    gender = models.PositiveIntegerField(choices=GENDER,default=UNISEX, blank=True, null=True)
    price = models.FloatField(default=0.0, null=True, blank=True)
    currency = models.CharField(max_length=10, default="USD")
    # Assets for try-on
    image = models.FileField(upload_to="products/images/", blank=True, null=True)  # 2D preview
    # model_3d = models.FileField(upload_to="products/models/", blank=True, null=True)  # e.g., .glb / .fbx for 3D try-on
    is_active = models.BooleanField(default=True)


    class Meta:
        db_table = 'product'

class FashionTipCategory(CommonInfo):
    """
    Categories like Summer, Winter, Street Style, Formal, etc.
    """
    name = models.CharField(max_length=100,blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'fashion_tip_category'


class FashionTip(CommonInfo):
    """
    Fashion tips, trends, and advice published by admin or influencers
    """
    title = models.CharField(max_length=200,blank=True, null=True)
    content = models.TextField()  # full text of the tip
    category = models.ForeignKey(FashionTipCategory, on_delete=models.SET_NULL, null=True,blank=True, related_name="tips")
    season = models.PositiveIntegerField(choices=WEATHER_TYPE,blank=True, null=True,default=ALL_SEASONS)
    style = models.PositiveIntegerField(choices=STYLE,default=CASUAL,blank=True, null=True)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)
    cover_image = models.FileField(upload_to="fashion_tips/images/", blank=True, null=True)

    class Meta:
        db_table = 'fashion_tip'


class PartnerStore(CommonInfo):
    name = models.CharField(max_length=255)
    website = models.URLField(blank=True, null=True)
    logo = models.FileField(upload_to="stores/logos/", blank=True, null=True)

    class  Meta:
        db_table = 'partner_store'

class DiscountAd(CommonInfo):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ManyToManyField(Image)
    discount_code = models.CharField(max_length=50, blank=True, null=True)
    partner_store = models.ForeignKey(PartnerStore, on_delete=models.CASCADE, related_name="discount_ads")
    target_segments = models.ManyToManyField(SubscriptionPlans, blank=True, related_name="discount_ads") #'Students', 'Premium Users', 'First-time Buyers'
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'discount_ad'