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
    
"""
Partner Store
"""
class PartnerStoreView(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        partner_store = PartnerStore.objects.all().order_by('-created_on')
        partner_store = query_filter_constructer(request,partner_store,{
            "name__icontains":"name",
            "website__icontains":"website",
            "created_on__date":"created_on",
        })

        if request.POST and not partner_store:
            messages.error(request, 'No Data Found')
        return render(request,'ecommerce/partner-store/partner-store.html',{
            "head_title":'Partner Store Management',
            "partner_store" : get_pagination(request, partner_store),
            "scroll_required":True if request.GET else False,
            "total_objects":partner_store.count()
        })
    
    @method_decorator(admin_only)
    def post(self, request, *args, **kwargs):
        store_id = request.POST.get('store_id')
        name = request.POST.get('name').strip()
        website = request.POST.get('website').strip()
        logo = request.FILES.get('logo')
        if store_id:
            try:
                partner_store = PartnerStore.objects.get(id=store_id)
            except PartnerStore.DoesNotExist:
                messages.error(request, "Partner store not found!")
                return redirect('ecommerce:partner_store')
            
            if PartnerStore.objects.filter(name=name, website=website).exclude(id=store_id).exists():
                messages.error(request, "Partner store already exists!")
                return redirect('ecommerce:partner_store')

            partner_store.name = name
            partner_store.website = website
            if logo:
                partner_store.logo = logo
            partner_store.save()
            messages.success(request, "Partner store updated successfully!")
        else:
            if PartnerStore.objects.filter(name=name, website=website).exists():
                messages.error(request, "Partner store already exists!")
                return redirect('ecommerce:partner_store')
            PartnerStore.objects.create(
                name=name,
                website=website,
                logo=logo
            )
            messages.success(request, "Partner store added successfully!")
        return redirect('ecommerce:partner_store')
    
class DeletePartnerStore(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        delete_store = PartnerStore.objects.get(id=self.kwargs['id']).delete()
        messages.success(request,'Partner Store Deleted Successfully!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    

"""
Discount Ads Management
"""
class DiscountAdsList(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        discount_ads = DiscountAd.objects.all().order_by('-created_on')
        discount_ads = query_filter_constructer(request,discount_ads,{
            "title__icontains":"title",
            "discount_code__icontains":"discount_code",
            "start_date__date":"start_date",
            "end_date__date":"end_date",
            "is_published":"is_published",
            "created_on__date":"created_on",
        })

        if request.POST and not discount_ads:
            messages.error(request, 'No Data Found')
        return render(request,'ecommerce/discount-ads/discount-list.html',{
            "head_title":'Discount Ads Management',
            "discount_ads" : get_pagination(request, discount_ads),
            "scroll_required":True if request.GET else False,
            "total_objects":discount_ads.count()
        })
    
class AddDiscountAd(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        partner_stores = PartnerStore.objects.all().order_by('-created_on')
        subscription_plans = SubscriptionPlans.objects.filter(status=True,is_deleted = False).order_by('-created_on')
        return render(request,'ecommerce/discount-ads/add-discount.html',{
            "stores":partner_stores,
            "subscription_plans":subscription_plans,
            "head_title":'Discount Ads Management',
        })
    
    def post(self,request,*args,**kwargs):
        store = get_object_or_404(PartnerStore, id=request.POST.get('store'))
        if DiscountAd.objects.filter(title=request.POST.get('title').strip(),target_segments__in = request.POST.getlist('target_sigment')).exists():
            messages.error(request, "Discount ads already exists!")
            return redirect('ecommerce:add_discount')
        
        discount_ad = DiscountAd.objects.create(
            title = request.POST.get('title').strip(),
            description = request.POST.get('description'),
            partner_store = store,
            
            discount_code = generate_discount_code(),
            start_date = request.POST.get('start_date'),
            end_date = request.POST.get('end_date'),
        )
        for seg_id in request.POST.getlist('target_sigment'):
            segment = SubscriptionPlans.objects.get(id=seg_id)
            discount_ad.target_segments.add(segment)
            
        for img in request.FILES.getlist('image'):
            discount_ad.image.add(Image.objects.create(image=img))

        discount_ad.save()
        messages.success(request, "Discount ads added successfully!")
        return redirect('ecommerce:view_discount',discount_ad.id)
    
class EditDiscountAd(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        partner_stores = PartnerStore.objects.all().order_by('-created_on')
        subscription_plans = SubscriptionPlans.objects.all()
        discount_ad = get_object_or_404(DiscountAd, id=self.kwargs['id'])
        return render(request, 'ecommerce/discount-ads/edit-discount.html', {
            "discount_ad": discount_ad,
            "stores": partner_stores,
            "subscription_plans": subscription_plans,
            "head_title": 'Discount Ads Management',
        })

    @method_decorator(admin_only)
    def post(self, request, *args, **kwargs):
        discount_ad = get_object_or_404(DiscountAd, id=self.kwargs['id'])
        store = get_object_or_404(PartnerStore, id=request.POST.get('store'))
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        title = request.POST.get('title', '').strip()
        target_segment_ids = request.POST.getlist('target_sigment')
        if DiscountAd.objects.filter(
            title=title,
            target_segments__in=target_segment_ids
        ).exclude(id=discount_ad.id).exists():
            messages.error(request, "Discount ad already exists!")
            return redirect('ecommerce:edit_discount', id=discount_ad.id)

        discount_ad.title = title
        discount_ad.description = request.POST.get('description')
        discount_ad.partner_store = store
        if start_date_str:
            discount_ad.start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        if end_date_str:
            discount_ad.end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        discount_ad.target_segments.set(target_segment_ids)
        if request.FILES.getlist('image'):
            for img in request.FILES.getlist('image'):
                discount_ad.image.add(Image.objects.create(image=img))
        discount_ad.save()
        messages.success(request, "Discount ad updated successfully!")
        return redirect('ecommerce:view_discount', discount_ad.id)

class ViewDiscountAd(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        discount_ad = DiscountAd.objects.get(id=self.kwargs['id'])
        return render(request,'ecommerce/discount-ads/view-discount.html',{
            "discount_ad":discount_ad,
            "head_title":'Discount Ads Management',
        })
    
class DeleteDiscountAd(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        discount_ad = DiscountAd.objects.get(id=self.kwargs['id']).delete()
        messages.success(request,message='Discount ads deleted successfully!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class PublishUnpublishDiscountAd(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        discount_ad = DiscountAd.objects.get(id=self.kwargs['id'])
        if discount_ad.is_published:
            discount_ad.is_published = False
            messages.success(request,'Discount ads marked as unpublish successfully')
        else:
            discount_ad.is_published = True
            discount_ad.published_at = datetime.now()
            messages.success(request,'Discount ads published successfully')
        discount_ad.save()
        return redirect('ecommerce:view_discount',id=discount_ad.id)