from django.shortcuts import render
from accounts.common_imports import *
from .models import *
from accounts.management.commands.default_data import default_activity_flags,default_hair_colors,default_skin_tones,default_body_types

# Create your views here.

"""
Partner Store
"""
class ClothCategoryView(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        cloth_category = ClothCategory.objects.all().order_by('-created_on')
        cloth_category = query_filter_constructer(request,cloth_category,{
            "title__icontains":"title",
            "created_on__date":"created_on",
        })

        if request.GET and not cloth_category:
            messages.error(request, 'No Data Found')
        return render(request,'wardrobe/wardrobe-essentials/cloth-category.html',{
            "head_title":'Cloth Category Management',
            "cloth_category" : get_pagination(request, cloth_category),
            "search_filters":request.GET.copy(),
            "scroll_required":True if request.GET else False,
            "total_objects":cloth_category.count()
        })
    
    @method_decorator(admin_only)
    def post(self, request, *args, **kwargs):
        category_id = request.POST.get('category_id')
        title = request.POST.get('title').strip()
        if category_id:
            try:
                cloth_category = ClothCategory.objects.get(id=category_id)
            except ClothCategory.DoesNotExist:
                messages.error(request, "Cloth Category not found!")
                return redirect('wardrobe:cloth_category')
            
            if ClothCategory.objects.filter(title=title).exclude(id=category_id).exists():
                messages.error(request, "Cloth Category already exists!")
                return redirect('wardrobe:cloth_category')

            cloth_category.title = title
            cloth_category.save()
            messages.success(request, "Cloth Category updated successfully!")
        else:
            if ClothCategory.objects.filter(title=title).exists():
                messages.error(request, "Cloth Category already exists!")
                return redirect('wardrobe:cloth_category')
            ClothCategory.objects.create(
                title=title
            )
            messages.success(request, "Cloth Category added successfully!")
        return redirect('wardrobe:cloth_category')
    
class DeleteClothCategory(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        cloth_category = ClothCategory.objects.get(id=self.kwargs['id']).delete()
        messages.success(request,'Cloth Category Deleted Successfully!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
"""
Occasion
"""
class OccasionView(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        occasion = Occasion.objects.all().order_by('-created_on')
        occasion = query_filter_constructer(request,occasion,{
            "title__icontains":"title",
            "created_on__date":"created_on",
        })

        if request.GET and not occasion:
            messages.error(request, 'No Data Found')
        return render(request,'wardrobe/wardrobe-essentials/occasion.html',{
            "head_title":'Occasion Management',
            "occasion" : get_pagination(request, occasion),
            "search_filters":request.GET.copy(),
            "scroll_required":True if request.GET else False,
            "total_objects":occasion.count()
        })
    
    @method_decorator(admin_only)
    def post(self, request, *args, **kwargs):
        occasion_id = request.POST.get('occasion_id')
        title = request.POST.get('title').strip()
        if occasion_id:
            try:
                occasion = Occasion.objects.get(id=occasion_id)
            except Occasion.DoesNotExist:
                messages.error(request, "Occasion not found!")
                return redirect('wardrobe:occasion')
            
            if Occasion.objects.filter(title=title).exclude(id=occasion_id).exists():
                messages.error(request, "Occasion already exists!")
                return redirect('wardrobe:occasion')

            occasion.title = title
            occasion.save()
            messages.success(request, "Occasion updated successfully!")
        else:
            if Occasion.objects.filter(title=title).exists():
                messages.error(request, "Occasion already exists!")
                return redirect('wardrobe:occasion')
            Occasion.objects.create(
                title=title
            )
            messages.success(request, "Occasion added successfully!")
        return redirect('wardrobe:occasion')
    
class DeleteOccasion(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        occasion = Occasion.objects.get(id=self.kwargs['id']).delete()
        messages.success(request,'Occasion Deleted Successfully!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class AccessoryView(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        accessory = Accessory.objects.all().order_by('-created_on')
        accessory = query_filter_constructer(request,accessory,{
            "title__icontains":"title",
            "created_on__date":"created_on",
        })

        if request.POST and not accessory:
            messages.error(request, 'No Data Found')
        return render(request,'wardrobe/wardrobe-essentials/accessory.html',{
            "head_title":'Accessory Management',
            "accessory" : get_pagination(request, accessory),
            "search_filters":request.GET.copy(),
            "scroll_required":True if request.GET else False,
            "total_objects":accessory.count()
        })
    
    @method_decorator(admin_only)
    def post(self, request, *args, **kwargs):
        accessory_id = request.POST.get('accessory_id')
        title = request.POST.get('title').strip()
        if accessory_id:
            try:
                accessory = Accessory.objects.get(id=accessory_id)
            except Accessory.DoesNotExist:
                messages.error(request, "Accessory not found!")
                return redirect('wardrobe:accessory')
            
            if Accessory.objects.filter(title=title).exclude(id=accessory_id).exists():
                messages.error(request, "Accessory already exists!")
                return redirect('wardrobe:accessory')

            accessory.title = title
            accessory.save()
            messages.success(request, "Accessory updated successfully!")
        else:
            if Accessory.objects.filter(title=title).exists():
                messages.error(request, "Accessory already exists!")
                return redirect('wardrobe:accessory')
            Accessory.objects.create(
                title=title
            )
            messages.success(request, "Accessory added successfully!")
        return redirect('wardrobe:accessory')
    
class DeleteAccessory(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        accessory = Accessory.objects.get(id=self.kwargs['id']).delete()
        messages.success(request,'Accessory Deleted Successfully!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    

class WardrobeList(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        wardrobs = Wardrobe.objects.all().order_by('-created_on')
        wardrobs = query_filter_constructer(request,wardrobs,{
            "name__icontains":"name",
            "user__full_name__icontains":"user__full_name",
            "is_shared":"is_shared",
        })

        if request.GET and not wardrobs:
            messages.error(request, 'No Data Found')
        return render(request,'wardrobe/wardrobs/wardrobe-list.html',{
            "head_title":'Wardrobe Management',
            "wardrobs" : get_pagination(request, wardrobs),
            "search_filters":request.GET.copy(),
            "scroll_required":True if request.GET else False,
            "total_objects":wardrobs.count()
        })
    
class WardrobeView(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        wardrobe = Wardrobe.objects.get(id=self.kwargs['id'])
        cloth_items = ClothingItem.objects.filter(wardrobe = wardrobe).order_by('-created_on')
        return render(request,'wardrobe/wardrobs/view-wardrobe.html',{
            "head_title":'Wardrobe Management',
            "wardrobe":wardrobe,
            "cloth_items":cloth_items
        })

class ActivityFlags(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        activity_flags = ActivityFlag.objects.all().order_by('-created_on')
        activity_flags = query_filter_constructer(request,activity_flags,{
            "name__icontains":"name",
            "description__icontains":"description",
            "created_on__date":"created_on"
        })
        if request.POST and not activity_flags:
            messages.error(request, 'No Data Found')
        return render(request,'ecommerce/trips/activity-flag.html',{
            "head_title":"Activity Flags Management",
            "activity_flags":get_pagination(request,activity_flags),
            "search_filters":request.GET.copy(),
            "total_objects":activity_flags.count()
        })
    
class DeleteActivityFlag(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        activity_flag = ActivityFlag.objects.get(id=self.kwargs.get('id'))
        activity_flag.delete()
        messages.success(request, "Flag deleted successfully !")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
class SyncDefaultActivityFlag(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        for activity in default_activity_flags:
            flag, created = ActivityFlag.objects.get_or_create(
                name=activity["name"],
                defaults={
                    "description": activity["description"],
                }
            )
        messages.success(request, "Activity Flag Sync successfully !")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class UserTrips(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        trips = Trips.objects.all().order_by('-created_on')
        trips = query_filter_constructer(request,trips,{
            "title__icontains":"title",
            "location__icontains":"location",
            "created_by__full_name":"created_by",
            "activity_flag__name":"activity_flag",
            "trip_length":"trip_length",
            "created_on__date":"created_on",
        })

        if request.POST and not trips:
            messages.error(request, 'No Data Found')
        return render(request,'ecommerce/trips/trips.html',{
            "head_title":'Trips Management',
            "trips" : get_pagination(request, trips),
            "search_filters":request.GET.copy(),
            "scroll_required":True if request.GET else False,
            "total_objects":trips.count()
        })

class ViewTripDetails(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        trip = Trips.objects.get(id=self.kwargs.get('id'))
        return render(request,'ecommerce/trips/view-trip-detail.html',{"trip":trip,"head_title":"Trips Management"})
    

class UserOutfit(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        outfits = Outfit.objects.all().order_by('-created_on')
        outfits = query_filter_constructer(request,outfits,{
            "title__icontains":"title",
            "occasion__title__icontains":"occasion",
            "created_by__full_name":"created_by",
            "season":"season",
            "created_on__date":"created_on",
        })

        if request.POST and not outfits:
            messages.error(request, 'No Data Found !')
        return render(request,'ecommerce/outfits/outfits.html',{
            "head_title":'Outfit Management',
            "outfits" : get_pagination(request, outfits),
            "search_filters":request.GET.copy(),
            "scroll_required":True if request.GET else False,
            "total_objects":outfits.count()
        })

class ViewOutfitDetails(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        outfit = Outfit.objects.get(id=self.kwargs.get('id'))
        return render(request,'ecommerce/outfits/view-outfit-detail.html',{"outfit":outfit,"head_title":"Outfit Management"})
    

class HairColorList(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        hair_colors  = HairColor.objects.filter(is_active=True).order_by('-created_on')
        hair_colors = query_filter_constructer(request,hair_colors,{
            "title__icontains":"title",
            "color_code":"color_code",
            "created_on__date":"created_on"
        })
        if request.GET and not hair_colors:
            messages.error(request, 'No Data Found')
        return render(request,'wardrobe/wardrobe-essentials/hair-color.html',{
            "head_title":'Hair Color Management',
            "hair_colors" : get_pagination(request, hair_colors),
            "search_filters":request.GET.copy(),
            "scroll_required":True if request.GET else False,
            "total_objects":hair_colors.count()
        })

class SkinToneList(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        skin_tones  = SkinTone.objects.filter(is_active=True).order_by('-created_on')
        skin_tones = query_filter_constructer(request,skin_tones,{
            "title__icontains":"title",
            "color_code":"color_code",
            "created_on__date":"created_on"
        })
        if request.GET and not skin_tones:
            messages.error(request, 'No Data Found')
        return render(request,'wardrobe/wardrobe-essentials/skin-tone.html',{
            "head_title":'Skin Tone Management',
            "skin_tones" : get_pagination(request, skin_tones),
            "search_filters":request.GET.copy(),
            "scroll_required":True if request.GET else False,
            "total_objects":skin_tones.count()
        })

class SyncDefaultHairColor(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        for hair_color in default_hair_colors:
            hair_color, created = HairColor.objects.get_or_create(
                title=hair_color["name"],
                defaults={
                    "color_code": hair_color["hex"],
                }
            )
        messages.success(request, "Hair Color Sync successfully !")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
class SyncDefaultSkinTone(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        for skin_tone in default_skin_tones:
            skin_tone, created = SkinTone.objects.get_or_create(
                title=skin_tone["name"],
                defaults={
                    "color_code": skin_tone["hex"],
                }
            )
        messages.success(request, "Skin Tone Sync successfully !")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class BodyTypeList(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        body_types  = BodyType.objects.filter(is_active=True).order_by('-created_on')
        body_types = query_filter_constructer(request,body_types,{
            "title__icontains":"title",
            "description__icontains":"description",
            "created_on__date":"created_on"
        })
        if request.GET and not body_types:
            messages.error(request, 'No Data Found')
        return render(request,'wardrobe/wardrobe-essentials/body-type.html',{
            "head_title":'Body Type Management',
            "body_types" : get_pagination(request, body_types),
            "search_filters":request.GET.copy(),
            "scroll_required":True if request.GET else False,
            "total_objects":body_types.count()
        })
    
    @method_decorator(admin_only)
    def post(self, request, *args, **kwargs):
        body_type_id = request.POST.get('body_type_id')
        if body_type_id:
            body_type = get_or_none(BodyType,'Body type does not exist !',id=body_type_id)
            if BodyType.objects.filter(title=request.POST.get('title')).exclude(id=body_type_id).exists():
                messages.error(request, "Body Type already exists!")
                return redirect('wardrobe:body_type_list')
            if request.POST.get('title'):
                body_type.title = request.POST.get('title').strip()
            if request.POST.get('description'):
                body_type.description = request.POST.get('description').strip()
            body_type.save()
            messages.success(request, "Body Type updated successfully!")
        else:
            if BodyType.objects.filter(title=request.POST.get('title')).exists():
                messages.error(request, "Body Type already exists!")
                return redirect('wardrobe:body_type_list')
            BodyType.objects.create(
                title=request.POST.get('title').strip(),
                description=request.POST.get('description').strip()
            )
            messages.success(request, "Body Type added successfully!")
        return redirect('wardrobe:body_type_list')

class SyncDefaultBodyType(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        for type in default_body_types:
            type, created = BodyType.objects.get_or_create(
                title=type["name"],
                defaults={
                    "color_code": type["description"],
                }
            )
        messages.success(request, "Body Type Sync successfully !")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class DeleteBodyType(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        body_type = BodyType.objects.get(id=self.kwargs.get('id'))
        body_type.delete()
        messages.success(request, "Body type deleted successfully !")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))