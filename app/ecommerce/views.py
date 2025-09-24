from django.shortcuts import render,get_object_or_404
from accounts.common_imports import *
from .models import *


class CategoryList(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        fashion_tip_categories = FashionTipCategory.objects.all().order_by('-created_on')
        fashion_tip_categories = query_filter_constructer(request,fashion_tip_categories,{
            "name__icontains":"name",
            "description__icontains":"description",
            "is_active":"is_active",
            "created_on__date":"created_on",

        })

        if request.POST and not fashion_tip_categories:
            messages.error(request, 'No Data Found')
        return render(request,'ecommerce/fashion-tip-category/category-list.html',{
            "head_title":'Fashion Tip category Management',
            "fashion_tip_categories" : get_pagination(request, fashion_tip_categories),
            "scroll_required":True if request.GET else False,
            "total_objects":fashion_tip_categories.count()
        })
    
class AddCategory(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        return render(request,'ecommerce/fashion-tip-category/add-category.html',{"head_title":'Fashion Tip category Management',})
    
    def post(self,request,*args,**kwargs):
        if FashionTipCategory.objects.filter(name=request.POST.get('name').strip()).exists():
            messages.success(request, "Category already exists!")
            return redirect('ecommerce:add_category')
        
        category = FashionTipCategory.objects.create(
            name = request.POST.get('name').strip(),
            description = request.POST.get('description')
        )
        messages.success(request, "Category added successfully!")
        return redirect('ecommerce:view_category',category.id)
    
class EditCategory(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        category = FashionTipCategory.objects.get(id=self.kwargs['id'])
        return render(request,'ecommerce/fashion-tip-category/edit-category.html',{
            "category":category,
            "head_title":'Fashion Tip category Management',
        })
    
    @method_decorator(admin_only)
    def post(self,request,*args,**kwargs):
        category = FashionTipCategory.objects.get(id=self.kwargs['id'])
        if FashionTipCategory.objects.filter(name = request.POST.get('name').strip()).exclude(id=category.id):
            messages.error(request,"Category already exists!")
            return redirect('ecommerce:edit_category',id=category.id)
        category.name = request.POST.get('name').strip()
        category.description = request.POST.get('description')
        category.save()
        messages.success(request, "Category updated successfully!")
        return redirect('ecommerce:view_category',category.id)

class ViewCategory(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        category = FashionTipCategory.objects.get(id=self.kwargs['id'])
        return render(request,'ecommerce/fashion-tip-category/view-category.html',{
            "category":category,
            "head_title":'Fashion Tip category Management',
        })

class DeleteCategory(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        category = FashionTipCategory.objects.get(id=self.kwargs['id']).delete()
        messages.success(request,message='Category deleted successfully!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class CategoryStatus(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        category = FashionTipCategory.objects.get(id=self.kwargs['id'])
        if category.is_active:
            category.is_active = False
            message="Category Deactivated Successfully!"
        else:
            category.is_active = True
            message="Category Activated Successfully!"
        category.save()
        messages.success(request,message=message)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
"""
Fashion Tips Management
"""
class FashionTipList(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        fashion_tips = FashionTip.objects.all().order_by('-created_on')
        fashion_tips = query_filter_constructer(request,fashion_tips,{
            "title__icontains":"title",
            "category__name__icontains":"category__name",
            "is_published":"is_published",
            "created_on__date":"created_on",
            'season':"season",
            'style':"style",
        })

        if request.POST and not fashion_tips:
            messages.error(request, 'No Data Found')
        return render(request,'ecommerce/fashion-tips/tip-list.html',{
            "head_title":'Fashion Tip Management',
            "fashion_tips" : get_pagination(request, fashion_tips),
            "scroll_required":True if request.GET else False,
            "total_objects":fashion_tips.count()
        })
    
class AddFashionTip(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        categories = FashionTipCategory.objects.filter(is_active=True).order_by('-created_on')
        return render(request,'ecommerce/fashion-tips/add-tip.html',{
            "categories":categories,
            "head_title":'Fashion Tip Management',
        })
    
    def post(self,request,*args,**kwargs):
        if not request.POST.get('category'):
            messages.error(request, "Please select a category.")
            return redirect('ecommerce:add_fashion_tip')

        category = get_object_or_404(FashionTipCategory, id=request.POST.get('category'))
        if FashionTip.objects.filter(title=request.POST.get('title').strip(),category = category,season = request.POST.get('season'),style = request.POST.get('style')).exists():
            messages.success(request, "Fashion tip already exists!")
            return redirect('ecommerce:add_fashion_tip')
        
        fashion_tip = FashionTip.objects.create(
            title = request.POST.get('title').strip(),
            content = request.POST.get('content'),
            category = category,
            season = request.POST.get('season'),
            style = request.POST.get('style'),
            cover_image = request.FILES.get('cover_image')
        )
        messages.success(request, "Fashion tip added successfully!")
        return redirect('ecommerce:view_fashion_tip',fashion_tip.id)
    
class EditFashionTip(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        categories = FashionTipCategory.objects.filter(is_active=True).order_by('-created_on')
        fashion_tip = FashionTip.objects.get(id=self.kwargs['id'])
        return render(request,'ecommerce/fashion-tips/edit-tip.html',{
            "fashion_tip":fashion_tip,
            "categories":categories,
            "head_title":'Fashion Tip Management',
        })
    
    @method_decorator(admin_only)
    def post(self,request,*args,**kwargs):
        fashion_tip = FashionTip.objects.get(id=self.kwargs['id'])
        category = FashionTipCategory.objects.get(id = request.POST.get('category'))
        if FashionTip.objects.filter(title=request.POST.get('title').strip(),category = request.POST.get('category'),season = request.POST.get('season'),style = request.POST.get('style')).exclude(id=fashion_tip.id):
            messages.error(request,"Fashion tip already exists!")
            return redirect('ecommerce:edit_fashion_tip',id=fashion_tip.id)
        
        if request.FILES.get('cover_image'):
            fashion_tip.cover_image = request.FILES.get('cover_image')
        fashion_tip.title = request.POST.get('title').strip()
        fashion_tip.content = request.POST.get('content')
        fashion_tip.category = category
        fashion_tip.season = request.POST.get('season')
        fashion_tip.style = request.POST.get('style')
        fashion_tip.save()
        messages.success(request, "Fashion tip updated successfully!")
        return redirect('ecommerce:view_fashion_tip',fashion_tip.id)

class ViewFashionTip(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        fashion_tip = FashionTip.objects.get(id=self.kwargs['id'])
        return render(request,'ecommerce/fashion-tips/view-tip.html',{
            "fashion_tip":fashion_tip,
            "head_title":'Fashion Tip Management',
        })
    
class DeleteFashionTip(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        fashion_tip = FashionTip.objects.get(id=self.kwargs['id']).delete()
        messages.success(request,message='Fashion tip deleted successfully!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class PublishUnpublishFashionTip(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        fashion_tip = FashionTip.objects.get(id=self.kwargs['id'])
        if fashion_tip.is_published:
            fashion_tip.is_published = False
            messages.success(request,'Fashion tip marked as unpublish successfully')
        else:
            fashion_tip.is_published = True
            fashion_tip.published_at = datetime.now()
            messages.success(request,'Fashion tip published successfully')
        fashion_tip.save()
        return redirect('ecommerce:view_fashion_tip',id=fashion_tip.id)