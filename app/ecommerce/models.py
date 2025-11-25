from django.db import models
from accounts.common_imports import *
from accounts.models import *
from accounts.constants import *
from subscription.models import *


class AffiliateNetwork(CommonInfo):
    name = models.CharField(max_length=100, null=True, blank=True)   # AWIN, CJ, Rakuten, Impact
    api_key = models.CharField(max_length=255, null=True, blank=True)
    publisher_id = models.CharField(max_length=100, null=True, blank=True)
    website_id = models.CharField(max_length=100, null=True, blank=True)
    token = models.CharField(max_length=255, null=True, blank=True)
    base_url = models.URLField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'affiliate_network'

class AffiliateAdvertiser(CommonInfo):
    network = models.ForeignKey(AffiliateNetwork, on_delete=models.CASCADE,null=True, blank=True)
    advertiser_id = models.CharField(max_length=100, null=True, blank=True)   # Provided by AWIN/CJ
    name = models.CharField(max_length=200, null=True, blank=True)            # Zara, H&M, Nike
    logo = models.URLField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'affiliate_advertiser'


class ProductCategory(CommonInfo):
    """
    Categories like Shirts, Jeans, Dresses, Accessories
    """
    name = models.CharField(max_length=100, unique=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL,null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'product_category'


class Product(CommonInfo):
    """
    Products managed by admin for virtual try-ons
    """
    advertiser = models.ForeignKey(AffiliateAdvertiser, on_delete=models.CASCADE,blank=True, null=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="products")
    product_id = models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=150,blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    size = models.CharField(max_length=50, blank=True, null=True)
    gender = models.PositiveIntegerField(choices=GENDER,default=UNISEX, blank=True, null=True)
    price = models.FloatField(default=0.0, null=True, blank=True)
    currency = models.CharField(max_length=10, null=True, blank=True)
    last_synced = models.DateTimeField(auto_now=True)
    product_id = models.CharField(max_length=200, null=True, blank=True)      # ID from affiliate network
    image_url = models.URLField(null=True, blank=True)
    product_url = models.URLField()                    # Original URL
    affiliate_url = models.URLField()                  # Tracking URL
    # Assets for try-on
    image = models.FileField(upload_to="products/images/", blank=True, null=True)  # 2D preview
    # model_3d = models.FileField(upload_to="products/models/", blank=True, null=True)  # e.g., .glb / .fbx for 3D try-on
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'product'


class AffiliateLink(CommonInfo):
    advertiser = models.ForeignKey(AffiliateAdvertiser, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True, blank=True)
    deeplink = models.URLField()
    enabled = models.BooleanField(default=True)

    class Meta:
        db_table = 'affiliate_link'


class AffiliateClick(CommonInfo):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    advertiser = models.ForeignKey(AffiliateAdvertiser, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    device = models.CharField(max_length=50, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        db_table = 'affiliate_click'

class AffiliateConversion(CommonInfo):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    advertiser = models.ForeignKey(AffiliateAdvertiser, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)

    order_id = models.CharField(max_length=200, null=True, blank=True)
    commission = models.FloatField(default=0.0)
    order_value = models.FloatField(default=0.0)
    currency = models.CharField(max_length=5, null=True, blank=True)

    transaction_time = models.DateTimeField()
    fetched_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'affiliate_conversion'


class AffiliateReport(CommonInfo):
    advertiser = models.ForeignKey(AffiliateAdvertiser, on_delete=models.CASCADE)
    clicks = models.IntegerField(default=0)
    conversions = models.IntegerField(default=0)
    revenue = models.FloatField(default=0.0)
    date = models.DateField()

    class Meta:
        db_table = 'affiliate_report'

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
    style = models.PositiveIntegerField(choices=STYLE,default=CASUAL,blank=True, null=True) # Casual,Formal,party,street style,slassic
    gender = models.PositiveIntegerField(choices=GENDER,default=OTHER,blank=True, null=True)
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