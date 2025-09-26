from django.shortcuts import render
from accounts.common_imports import *
from .models import *

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

        if request.POST and not cloth_category:
            messages.error(request, 'No Data Found')
        return render(request,'wardrobe/wardrobe-essentials/cloth-category.html',{
            "head_title":'Cloth Category Management',
            "cloth_category" : get_pagination(request, cloth_category),
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

        if request.POST and not occasion:
            messages.error(request, 'No Data Found')
        return render(request,'wardrobe/wardrobe-essentials/occasion.html',{
            "head_title":'Occasion Management',
            "occasion" : get_pagination(request, occasion),
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
