from django.shortcuts import render
from accounts.common_imports import *
from accounts.utils import *
from .models import *
from django.core.files.base import ContentFile
from api.avatar import *


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
            "search_filters":request.GET.copy(),
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
        return redirect('ecommerce:fashion_category_list')

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
            "search_filters":request.GET.copy(),
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
        # if not request.POST.get('category'):
        #     messages.error(request, "Please select a category.")
        #     return redirect('ecommerce:add_fashion_tip')

        # category = get_object_or_404(FashionTipCategory, id=request.POST.get('category'))
        if FashionTip.objects.filter(title=request.POST.get('title').strip(),season = request.POST.get('season'),style = request.POST.get('style')).exists():
            messages.success(request, "Fashion tip already exists!")
            return redirect('ecommerce:add_fashion_tip')
        
        fashion_tip = FashionTip.objects.create(
            title = request.POST.get('title').strip(),
            content = request.POST.get('content'),
            season = request.POST.get('season'),
            style = request.POST.get('style'),
            cover_image = request.FILES.get('cover_image'),
            gender = request.POST.get('gender')
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
        # category = FashionTipCategory.objects.get(id = request.POST.get('category'))
        if FashionTip.objects.filter(title=request.POST.get('title').strip(),season = request.POST.get('season'),style = request.POST.get('style')).exclude(id=fashion_tip.id):
            messages.error(request,"Fashion tip already exists!")
            return redirect('ecommerce:edit_fashion_tip',id=fashion_tip.id)
        
        if request.FILES.get('cover_image'):
            fashion_tip.cover_image = request.FILES.get('cover_image')
        if request.POST.get('title'):
            fashion_tip.title = request.POST.get('title').strip()
        if request.POST.get('content'):
            fashion_tip.content = request.POST.get('content')
        # if request.POST.get('category'):
        #     fashion_tip.category = category
        if request.POST.get('season'):
            fashion_tip.season = request.POST.get('season')
        if request.POST.get('style'):
            fashion_tip.style = request.POST.get('style')
        if request.POST.get('gender'):
            fashion_tip.gender = request.POST.get('gender')
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
        return redirect('ecommerce:fashion_tip_list')
    
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
            "search_filters":request.GET.copy(),
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
            "search_filters":request.GET.copy(),
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
        store = PartnerStore.objects.get(id=request.POST.get('store'))
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
        discount_ad = DiscountAd.objects.get(id=self.kwargs['id'])
        return render(request, 'ecommerce/discount-ads/edit-discount.html', {
            "discount_ad": discount_ad,
            "stores": partner_stores,
            "subscription_plans": subscription_plans,
            "head_title": 'Discount Ads Management',
        })

    @method_decorator(admin_only)
    def post(self, request, *args, **kwargs):
        discount_ad = DiscountAd.objects.get(id=self.kwargs['id'])
        store = PartnerStore.objects.get(id=request.POST.get('store'))
        title = request.POST.get('title', '').strip()
        target_segment_ids = request.POST.getlist('target_sigment')

        if DiscountAd.objects.filter(title=title,target_segments__in=target_segment_ids).exclude(id=discount_ad.id).exists():
            messages.error(request, "Discount ad already exists!")
            return redirect('ecommerce:edit_discount', id=discount_ad.id)

        discount_ad.title = title
        if request.POST.get('description'):
            discount_ad.description = request.POST.get('description')
        if request.POST.get('store'):
            discount_ad.partner_store = store
        if request.POST.get('start_date'):
            discount_ad.start_date = datetime.strptime(request.POST.get('start_date'), '%Y-%m-%d')
        if request.POST.get('end_date'):
            discount_ad.end_date = datetime.strptime(request.POST.get('end_date'), '%Y-%m-%d')
        if request.POST.getlist('target_sigment'):
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
        return redirect('ecommerce:discount_list')

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
    


#Add marketing data from admin  
class AffiliateMarketingTools(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        marketing_categories=MarketingToolsCategories.objects.all().order_by('-created_on')
        marketing_categories = query_filter_constructer(request,marketing_categories,
                {
                    "title__icontains":"title",
                    "created_on__date":"created_on",
                }
            )
        if request.GET and not marketing_categories:
            messages.error(request, 'No Data Found!')
        guide=AffiliateGuide.objects.first()
        return render(request,'users/affiliate/admin/markteing_tools/marketing-tools.html',{
            "head_title":'Affiliate Management',
            "marketing_categories":marketing_categories,
            'sort_params':request.GET.copy(),
            "guide":guide
        })
    
    def post(self, request, *args, **kwargs):
        if not request.POST.get('marketing_category'):
            messages.error(request,'Please enter marketing category')
        else:
            marketing_category,created=MarketingToolsCategories.objects.get_or_create(title=request.POST.get('marketing_category').strip())
            if created:
                marketing_category.save()
                messages.success(request,'Marketing category added successfully!')
            else:
                messages.success(request,'Marketing category already exists!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class UpdateMarketingCategory(View):
    @method_decorator(admin_only)
    def post(self, request, *args, **kwargs):
        marketing_category = MarketingToolsCategories.objects.get(id=request.POST.get('category_id'))
        if MarketingToolsCategories.objects.filter(title=request.POST.get('e_category_title').strip()).exclude(id=marketing_category.id):
            messages.error(request,'Marketing category Already Exists!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if request.POST.get('e_category_title'):
            marketing_category.title=request.POST.get('e_category_title')

        marketing_category.save()
        messages.success(request, 'Marketing category updated successfully!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    

class DeleteMarketingCategory(View):
    def get(self,request,*args,**kwargs):
        MarketingToolsCategories.objects.get(id=self.kwargs['id']).delete()
        messages.success(request, 'Marketing category deleted successfully!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 

   
class ViewMarketingCategory(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        marketing_category = MarketingToolsCategories.objects.get(id=self.kwargs['id'])
        category_media=marketing_category.category_media.all().order_by('-created_on')

        category_media = query_filter_constructer(request,category_media,
                {
                    "name__icontains":"name",
                    "created_on__date":"created_on",
                }
            )
        if request.GET and not category_media:
            messages.error(request, 'No Data Found!')
    
        return render(request,'users/affiliate/admin/markteing_tools/category_media.html',{
            'head_title':'Affiliate Management',
            'marketing_category':marketing_category,
            'category_media':get_pagination(request,category_media),
            "sort_params":request.GET
              })


class AddMarketingCatyegoryMedia(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        marketing_category = MarketingToolsCategories.objects.get(id=self.kwargs['id'])
        return render(request, 'users/affiliate/admin/markteing_tools/add_category_media.html',{"head_title":"Affiliate Management","marketing_category":marketing_category})

    @method_decorator(admin_only)
    def post(self, request, *args, **kwargs):
        marketing_category = MarketingToolsCategories.objects.get(id=self.kwargs['id'])
        if not request.POST.get('name'):
            messages.error(request,'Please enter media name')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        media_file = request.FILES.get('media_file')
        link = request.POST.get('link')
        if media_file and link:
            messages.error(request, 'Please provide only one input: either a media file or a link, not both.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if not media_file and not link:
            messages.error(request, 'Please provide at least one input: a media file or a link.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        category_media = MarketingCategoryMedia.objects.create(
            category=marketing_category,
            name = request.POST.get('name'),
            media_file = request.FILES.get('media_file'),
            link=request.POST.get('link')
        )
        messages.success(request, 'Category Media added successfully!')
        return redirect('affiliate_v2:view_marketing_category',id=marketing_category.id)
    

class UpdateMarketingCatyegoryMedia(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        category_media = MarketingCategoryMedia.objects.get(id=self.kwargs['id'])
        return render(request, 'users/affiliate/admin/markteing_tools/update_category_media.html',{"head_title":"Affiliate Management","category_media":category_media})

    @method_decorator(admin_only)
    def post(self, request, *args, **kwargs):
        category_media = MarketingCategoryMedia.objects.get(id=self.kwargs['id'])
        if MarketingCategoryMedia.objects.filter(category=category_media.category,name=request.POST.get('name').strip()).exclude(id=category_media.id):
            messages.error(request,'Category Media Already Exists!')
            return redirect('affiliate_v2:view_marketing_category',id=category_media.category.id)
        media_file = request.FILES.get('media_file')
        link = request.POST.get('link')
        if media_file and link:
            messages.error(request, 'Please provide only one input: either a media file or a link, not both.')
            return redirect('affiliate_v2:view_marketing_category', id=category_media.category.id)

        if not media_file and not link:
            messages.error(request, 'Please provide at least one input: a media file or a link.')
            return redirect('affiliate_v2:view_marketing_category', id=category_media.category.id)
        category_media.name=request.POST.get('name')
        category_media.media_file=media_file
        category_media.link=link
        category_media.save()
        messages.success(request, 'Category Media updated successfully!')
        return redirect('affiliate_v2:view_marketing_category',id=category_media.category.id)

class DeleteMarketingCatyegoryMedia(View):
    def get(self,request,*args,**kwargs):
        MarketingCategoryMedia.objects.get(id=self.kwargs['id']).delete()
        messages.success(request, 'Marketing category media deleted successfully!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
    

class AddAffiliateGuide(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        return render(request, 'users/affiliate/admin/guide/add_affiliate_guide.html',{"head_title":"Affiliate Management"})

    @method_decorator(admin_only)
    def post(self, request, *args, **kwargs):
        if not request.POST.get('description'):
            messages.error(request, 'please add guide description!')
            return redirect('affiliate_v2:affiliate_marketing_tools')
        if not AffiliateGuide.objects.first():
            AffiliateGuide.objects.create(description=request.POST.get('description'),image=request.FILES.get('image'))
            messages.success(request, 'Guide added successfully!')
        else:
            messages.error(request, 'Guide already exists!')
        return redirect('affiliate_v2:affiliate_marketing_tools')
    
class EditAffiliateGuide(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        guide=AffiliateGuide.objects.first()
        return render(request, 'users/affiliate/admin/guide/edit_affiliate_guide.html',{"head_title":"Affiliate Management","guide":guide})

    @method_decorator(admin_only)
    def post(self, request, *args, **kwargs):
        guide=AffiliateGuide.objects.first()
        if request.POST.get('description'):
            guide.description=request.POST.get('description')
        if request.FILES.get('image'):
            guide.image=request.FILES.get('image')
        guide.save()
        messages.success(request, 'Guide updated successfully!')
        return redirect('affiliate_v2:affiliate_marketing_tools')
    
class DeleteAffiliateGuide(View):
    def get(self,request,*args,**kwargs):
        try:
            AffiliateGuide.objects.first().delete()
            messages.success(request, 'Guide deleted successfully!')
        except:
            pass
        return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 


"""
Store Credentials
"""
class StoreCredentialsView(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        store_creds = StoreCredentials.objects.all().order_by('-created_on')
        return render(request,'ecommerce/partner-store/partner-store.html',{
            "head_title":'Store credentials Management',
            "store_creds" : get_pagination(request, store_creds),
            "scroll_required":True if request.GET else False,
            "total_objects":store_creds.count()
        })
    
    @method_decorator(admin_only)
    def post(self, request, *args, **kwargs):
        store_id = request.POST.get('store_id')
        access_token = request.POST.get('access_token').strip()
        refresh_token = request.POST.get('refresh_token').strip()
        url = request.FILES.get('url')
        if store_id:
            try:
                store_creds = StoreCredentials.objects.get(id=store_id)
            except StoreCredentials.DoesNotExist:
                messages.error(request, "Store credentials store not found!")
                return redirect('ecommerce:store_creds')
            
            if StoreCredentials.objects.filter(access_token=access_token, refresh_token=refresh_token).exclude(id=store_id).exists():
                messages.error(request, "Store credentials store already exists!")
                return redirect('ecommerce:store_creds')

            store_creds.access_token = access_token
            store_creds.refresh_token = refresh_token
            store_creds.url = url
            store_creds.save()
            messages.success(request, "Store credentials store updated successfully!")
        else:
            if StoreCredentials.objects.filter(access_token=access_token, refresh_token=refresh_token).exists():
                messages.error(request, "Store credentials store already exists!")
                return redirect('ecommerce:store_creds')
            StoreCredentials.objects.create(
                access_token=access_token,
                refresh_token=refresh_token,
                url = url,
                created_by = request.user
            )
            messages.success(request, "Store credentials added successfully!")
        return redirect('ecommerce:store_creds')
    
class DeleteStoreCredentials(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        delete_store = StoreCredentials.objects.get(id=self.kwargs['id']).delete()
        messages.success(request,'Store credentials Deleted Successfully!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
class UserFeedBackList(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        item_id = ClothingItem.objects.get(id = self.kwargs.get('id'))
        ratings = Rating.objects.filter(item=item_id).order_by('-created_on')
        return render(request, 'ecommerce/user-rating/user-rating-list.html',{
            "head_title":'Feedback Management',
            "item_id":item_id,
            "ratings":get_pagination(request,ratings),
            "scroll_required":True if request.GET else False,
            "search_filters":request.GET.copy(),
            "total_objects":ratings.count()
        })
    

class VirtualTryOnList(View):
    @method_decorator(admin_only)
    def get(self,request,*args,**kwargs):
        virtual_try_ons = VirtualTryOn.objects.all().order_by('-created_on')
        virtual_try_ons = query_filter_constructer(request,virtual_try_ons,{
            "order_id":"order_id",
            "user__full_name__icontains":"user",
            "sigmentation_type":"sigmentation_type",
            "status":"status",
            "created_on__date":"created_on",
        })

        if request.POST and not virtual_try_ons:
            messages.error(request, 'No Data Found')
        return render(request,'ecommerce/virtual-try-on/try-on-list.html',{
            "head_title":'Virtual Try On Management',
            "virtual_try_ons" : get_pagination(request, virtual_try_ons),
            "scroll_required":True if request.GET else False,
            "search_filters":request.GET.copy(),
            "total_objects":virtual_try_ons.count()
        })
    
class ViewTryOnDetails(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        virtual_try_on = VirtualTryOn.objects.get(id=self.kwargs['id'])
        return render(request,'ecommerce/virtual-try-on/try-on-details.html',{
            'head_title':'Virtual Try On Management',
            'virtual_try_on':virtual_try_on})


class DeleteVirtualTryOn(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        virtual_try_on = VirtualTryOn.objects.get(id=self.kwargs['id']).delete()
        messages.success(request,'Virtual Try On Deleted Successfully!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
class SyncTryOnData(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        try_ons = VirtualTryOn.objects.filter(status=None).order_by('created_on')
        order_ids = try_ons.values_list('order_id',flat=True)
        for order_id in order_ids:
            try:
                virtual_try_on = VirtualTryOn.objects.filter(order_id=order_id).first()
            except Exception as e:
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            if virtual_try_on.order_id:
                avatar_result = None
                order_status = check_lightx_order_status(virtual_try_on.order_id)
                try:
                    if order_status['data']['status'] == 'FAIL':
                        messages.error(request,order_status['data']['message'])
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                except:
                    pass
                if order_status['data']['body']['status'] == 'failed':
                    virtual_try_on.status = TRY_ON_PROCESSING
                    virtual_try_on.error_message = order_status['data']['statusCode']
                    virtual_try_on.save()
                    messages.error(request,order_status['data']['message'])
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
                body = order_status["data"]["body"]
                status_data = body.get("status")
                output = body.get("output")

                if output and status_data in ["active", "success"]:
                    avatar_result = order_status
                    break

                if status_data in ["failed", "error"]:
                    virtual_try_on.status = TRY_ON_FAILED
                    virtual_try_on.save()
                    messages.error(request,'Virtual try on generation failed')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

                if not avatar_result:
                    messages.error(request,'Virtual try on still processing. Try again later.')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

                image_url = avatar_result["data"]["body"]["output"]
                img_response = requests.get(image_url)
                if img_response.status_code != 200:
                    messages.error(request,'Failed to download virtual try on image')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

                file_name = image_url.split("/")[-1]
                virtual_try_on.output_image.save(file_name, ContentFile(img_response.content))
                virtual_try_on.status = TRY_ON_SUCCESS
                virtual_try_on.error_message = order_status['data']['statusCode']
                virtual_try_on.save()

                send_notification(
                    created_by=request.user,
                    created_for=[virtual_try_on.user.id],
                    title="New Virtual Try On Generated",
                    description=f"A new virtual try on is ready for {virtual_try_on.user.full_name}.",
                    notification_type=ADMIN_NOTIFICATION,
                    obj_id=str(virtual_try_on.user.id),
                )
        messages.success(request,"Virtual Try On Sync Successfully!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    


class SyncVirtualTryOnOutput(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        try_ons = VirtualTryOn.objects.get(id=self.kwargs.get('id'))
        if try_ons.order_id:
            order_status = check_lightx_order_status(try_ons.order_id)
            try:
                if order_status['data']['status'] == 'FAIL':
                    messages.error(request,order_status['data']['message'])
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            except:
                pass
            if order_status['data']['body']['status'] == 'failed':
                try_ons.status = TRY_ON_PROCESSING
                try_ons.error_message = order_status['data']['statusCode']
                try_ons.save()
                messages.error(request,order_status['data']['message'])
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
            body = order_status["data"]["body"]
            status_data = body.get("status")

            if status_data in ["failed", "error"]:
                try_ons.status = TRY_ON_FAILED
                try_ons.save()
                messages.error(request,'Virtual try on generation failed')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            image_url = order_status["data"]["body"]["output"]
            img_response = requests.get(image_url)
            if img_response.status_code != 200:
                messages.error(request,'Failed to download virtual try on image')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            file_name = image_url.split("/")[-1]
            try_ons.output_image.save(file_name, ContentFile(img_response.content))
            try_ons.status = TRY_ON_SUCCESS
            try_ons.error_message = order_status['data']['statusCode']
            try_ons.save()

            send_notification(
                created_by=request.user,
                created_for=[try_ons.user.id],
                title="New Virtual Try On Generated",
                description=f"A new virtual try on is ready for {try_ons.user.full_name}.",
                notification_type=ADMIN_NOTIFICATION,
                obj_id=str(try_ons.user.id),
            )
        messages.success(request,"Virtual Try On Sync Successfully!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


