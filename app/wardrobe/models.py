from django.db import models
from accounts.common_imports import *

class Wardrobe(CommonInfo):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wardrobes")
    name = models.CharField(max_length=100, default="My Wardrobe",blank=True, null=True)
    is_shared = models.BooleanField(default=False)
    shared_with = models.ManyToManyField(User, blank=True, related_name="shared_wardrobes")

    class Meta:
        db_table = 'wardrobe'


class ClothingItem(CommonInfo):
    wardrobe = models.ForeignKey(Wardrobe, on_delete=models.CASCADE, related_name="items",blank=True, null=True)
    image = models.ImageField(upload_to="wardrobe/items/",blank=True, null=True)
    ai_category = models.CharField(max_length=50, blank=True, null=True)
    manual_category = models.CharField(max_length=50,blank=True, null=True)
    weather_type = models.PositiveIntegerField(choices=WEATHER_TYPE,blank=True, null=True)
    color = models.CharField(max_length=30)
    brand = models.CharField(max_length=50, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    last_worn = models.DateTimeField(blank=True, null=True)
    wear_count = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'clothing_item'

    def cost_per_wear(self):
        if self.price and self.wear_count > 0:
            return round(self.price / self.wear_count, 2)
        return None

class Occasion(CommonInfo):
    clothing_item = models.ForeignKey(ClothingItem, on_delete=models.CASCADE, related_name="occasion",blank=True, null=True)
    title = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'occasion'

class Accessory(models.Model):
    clothing_item = models.ForeignKey(ClothingItem, on_delete=models.CASCADE, related_name="accessories",blank=True, null=True)
    type = models.CharField(max_length=50,blank=True, null=True)  # e.g., Watch, Sunglasses

    class Meta:
        db_table = 'accessories'

class Outfit(models.Model):
    wardrobe = models.ForeignKey(Wardrobe, on_delete=models.CASCADE, related_name="outfits",blank=True, null=True)
    items = models.ManyToManyField(ClothingItem, related_name="outfits",blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="created_outfits")
    notes = models.TextField(blank=True, null=True)  # Style suggestions
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'outfit'

class WearLog(models.Model):
    clothing_item = models.ForeignKey(ClothingItem, on_delete=models.CASCADE, related_name="wear_logs",blank=True, null=True)
    date_worn = models.DateField()
    occasion = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'wearLog'