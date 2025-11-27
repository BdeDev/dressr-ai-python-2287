from accounts.common_imports import *
from static_pages.models import *
from contact_us.models import ContactDetails,ContactUs
db_logger = logging.getLogger('db')
 

class index(View):
    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            user = request.user
            if user.is_superuser and user.role_id == ADMIN:
                return redirect('admin:index')
            return redirect('accounts:login')
        return render(request, "frontend/index.html", {"showclass":True})

def handler404(request, exception, template_name="frontend/404.html"):
    db_logger.exception(exception)
    return render(request, template_name, status=404)

def handler500(request, *args, **kwargs):
    db_logger.exception(Exception)
    return render(request, 'frontend/404.html', status=500)

def handler403(request, exception, template_name="frontend/404.html"):
    db_logger.exception(exception)
    return render(request, template_name, status=403)

def handler400(request, exception, template_name="frontend/404.html"):
    db_logger.exception(exception)
    return render(request, template_name, status=400)

class AboutUsview(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('frontend:index')
        about_us = Pages.objects.filter(type_id=ABOUT_US).first()
        return render(request, "frontend/about-us.html",{"data":about_us, "page_title":"About Us"})
    
# class ContactUsview(View):
#     def get(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return redirect('frontend:index')
#         contact_us = Pages.objects.filter(type_id=CONTACT_US).first()
#         return render(request, "frontend/contact-us.html",{"data":contact_us, "page_title":"Contact Us"})
    

class ContactUsView(View):
    def get(self, request, *args, **kwargs):
        contact_detail=ContactDetails.objects.first()
        return render(request, 'frontend/contact-us.html',{
            "head_title":"Contact Us",
            "contact_detail":contact_detail

        })
    def post(self, request, *args, **kwargs):
        if not (request.POST.get('full_name') and request.POST.get('email') and request.POST.get('message')):
            messages.error(request,"All fields are required!") 
            return redirect('frontend:index')
        ContactUs.objects.create(
            full_name = request.POST.get('full_name').strip(),
            email = request.POST.get('email').strip(),
            subject = request.POST.get('subject'),
            message = request.POST.get('message')
        )
        messages.success(request,"Thank you for contacting us. We will get back to you shortly!")
        return redirect('frontend:index')
    

class PrivacyPolicyview(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('frontend:index')
        privacy_policy = Pages.objects.filter(type_id=PRIVACY_POLICY).first()
        return render(request, "frontend/privacy_policy.html",{"data":privacy_policy, "page_title":"Privacy Policy"})
    
class TermsAndConditionsView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('frontend:index')
        terms_view = Pages.objects.filter(type_id=TERMS_AND_CONDITION).first()
        return render(request, "frontend/terms_condition.html",{"data":terms_view, "page_title":"Terms and Condition"})
    

class HowItWorksView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('frontend:index')
        How_it_works = Pages.objects.filter(type_id=HOW_IT_WORKS).first()
        faqs = FAQs.objects.all().order_by('created_on')
        return render(request, "frontend/how_it_works.html",{"data":How_it_works, "page_title":"How it works","faqs":faqs})
    
class PricingView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('frontend:index')
        Pricing = Pages.objects.filter(type_id=PRICING).first()
        return render(request, "frontend/pricing.html",{"data":Pricing, "page_title":"Pricing"})