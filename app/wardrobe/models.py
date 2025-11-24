from django.db import models
from accounts.common_imports import *
from accounts.models import CommonInfo,User

class Wardrobe(CommonInfo):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wardrobes",blank=True,null=True)
    name = models.CharField(max_length=100, default="My Wardrobe",blank=True, null=True)
    is_shared = models.BooleanField(default=False)
    shared_with = models.ManyToManyField(User, blank=True,related_name="shared_wardrobes")

    class Meta:
        db_table = 'wardrobe'

class ClothCategory(CommonInfo):
    title = models.CharField(max_length=100, blank=True, null=True)
    icon = models.FileField(upload_to="wardrobe/icons/",blank=True, null=True)

    class Meta:
        db_table = 'cloth_category'

class Occasion(CommonInfo):
    title = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'occasion'

class Accessory(CommonInfo):
    title = models.CharField(max_length=50,blank=True, null=True)  # e.g., Watch, Sunglasses

    class Meta:
        db_table = 'accessories'

class Tag(CommonInfo):
    title = models.CharField(max_length=50,blank=True, null=True)

    class Meta:
        db_table = 'tag'

class ClothingItem(CommonInfo):
    title = models.CharField(max_length=200,blank=True, null=True)
    wardrobe = models.ForeignKey(Wardrobe, on_delete=models.CASCADE, related_name="items",blank=True, null=True)
    image = models.FileField(upload_to="wardrobe/items/",blank=True, null=True)
    cloth_category = models.ForeignKey(ClothCategory,on_delete=models.SET_NULL, null=True,blank=True)
    occasion = models.ForeignKey(Occasion,on_delete=models.SET_NULL, null=True,blank=True)
    accessory = models.ForeignKey(Accessory,on_delete=models.SET_NULL,null=True,blank=True)
    # ai_category = models.CharField(max_length=50, blank=True, null=True)
    # manual_category = models.CharField(max_length=50,blank=True, null=True)
    weather_type = models.PositiveIntegerField(choices=WEATHER_TYPE,blank=True, null=True)
    color = models.CharField(max_length=30,blank=True, null=True)
    price = models.FloatField(default=0.0, null=True, blank=True)
    brand = models.CharField(max_length=50, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    last_worn = models.DateTimeField(blank=True, null=True)
    wear_count = models.PositiveIntegerField(default=0)
    favourite = models.ManyToManyField(User, related_name='favourite_item')
    item_url = models.URLField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name="items")

    class Meta:
        db_table = 'clothing_item'

    def cost_per_wear(self):
        if self.price and self.wear_count > 0:
            return round(self.price / self.wear_count, 2)
        return None

class Outfit(CommonInfo):
    title = models.CharField(max_length=200,blank=True, null=True)
    items = models.ManyToManyField(ClothingItem, related_name="outfits",blank=True)
    occasion = models.ForeignKey(Occasion,on_delete=models.SET_NULL, null=True,blank=True)
    weather_type = models.PositiveIntegerField(choices=WEATHER_TYPE,blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="created_outfits")
    color = models.CharField(max_length=30,blank=True, null=True)
    notes = models.TextField(blank=True, null=True)  # Style suggestions
    favourite = models.ManyToManyField(User, related_name='favourite_outfit')
    image = models.FileField(upload_to="wardrobe/outfit_image/",blank=True, null=True)

    class Meta:
        db_table = 'outfit'

class WearHistory(CommonInfo):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    outfit = models.ForeignKey(Outfit, on_delete=models.SET_NULL, null=True, blank=True)
    item = models.ForeignKey(ClothingItem, on_delete=models.CASCADE, null=True, blank=True)
    worn_on = models.DateField()
    notes = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'wear_history'
        unique_together = ('user', 'item', 'worn_on')

class ActivityFlag(CommonInfo):
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    create_by = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, related_name="activity_flag")

    class Meta:
        db_table = 'activity_flag'

class Trips(CommonInfo):
    outfit = models.ManyToManyField(Outfit)
    title = models.CharField(max_length=200,blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    location = models.TextField(null=True,blank=True)
    latitude=models.FloatField(null=True,blank=True)
    longitude=models.FloatField(null=True,blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,related_name="created_trips")
    activity_flag = models.ManyToManyField(ActivityFlag)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    trip_length = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'trip'
        
# class PackingItem(CommonInfo):
#     name = models.CharField(max_length=255,null=True, blank=True)
#     category = models.PositiveIntegerField(default=CLOTHING,choices=PACKING_CATEGORY,blank=True, null=True)
#     activity_flag = models.ForeignKey(ActivityFlag, on_delete=models.SET_NULL, null=True, blank=True)

#     class Meta:
#         db_table = 'packing_item'

class Recommendation(CommonInfo):
    vacation_plan = models.ForeignKey(Trips, on_delete=models.CASCADE, related_name="recommendations",blank=True, null=True)
    recommended_item = models.CharField(max_length=255,blank=True, null=True)
    category = models.PositiveIntegerField(choices=PACKING_CATEGORY,blank=True, null=True)
    purchase_link = models.URLField(blank=True, null=True)

    class Meta:
        db_table = 'recomendation'


class RecentSearch(CommonInfo):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recent_searches")
    keyword = models.CharField(max_length=255)

    class Meta:
        db_table = 'recent_search'