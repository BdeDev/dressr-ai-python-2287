from accounts.utils import get_pagination
from .models import *
from accounts.common_imports import *
from django.http import HttpResponseRedirect


"""
Page Management
"""
class PagesListView(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        pages = Pages.objects.all().order_by('-created_on').only('id')
        pages = query_filter_constructer(request, pages,
            {
                "id": "id",
                "title__icontains": "title",
                "content__icontains": "content",
                "type_id": "type_id",
                "is_active": "is_active",
                "created_on__date": "created_on",
            })

        if not pages and request.GET:
            messages.error(request, 'No Data Found')
        return render(request, 'StaticPages/pages-list.html',{
            "head_title":"Pages Management",
            "pages":get_pagination(request, pages),
            "search_filters":request.GET.copy(),
            "total_objects": pages.count(),
        })


class ViewPage(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        page = Pages.objects.get(id=self.kwargs['id'])
        return render(request, 'StaticPages/view-page.html',{"page":page,"head_title":"Pages Management"})


class AddPageView(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        # Get the set of existing type_ids from the Pages class
        existing_types = set(Pages.objects.all().values_list('type_id', flat=True))
        pages = [
            {"key": 1, "value": "Terms & Conditions"},
            {"key": 2, "value": "Privacy Policy"},
            {"key": 3, "value": "About Us"},
            {"key": 4, "value": "How It Works"},
            {"key": 5, "value": "Cookie Policy"}
        ]
        # Filter the pages list to remove items with keys that exist in existing_types
        pages = [page for page in pages if page["key"] not in existing_types]
        return render(request, 'StaticPages/add-page.html',{"head_title":"Pages Management","pages":pages})
    @method_decorator(admin_only)
    def post(self, request, *args, **kwargs):
        title = request.POST.get("title")
        content = request.POST.get("content")
        type_id = request.POST.get("type_id")

        if Pages.objects.filter(type_id = type_id):
            messages.error(request, 'Page already exists!')
            return render(request, 'StaticPages/add-page.html', {
                "title": title, "content": content, "type_id": type_id, "head_title": "Pages"})

        page = Pages.objects.create(
            title=title,
            type_id=type_id,
            content=content
        )
        messages.success(request, 'Page added successfully!')
        return redirect('static_pages:view_page',id=page.id)


class EditPage(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        page = Pages.objects.get(id=self.kwargs['id'])
        return render(request, 'StaticPages/edit-page.html',{"head_title":"Pages Management","page":page})
    @method_decorator(admin_only)
    def post(self, request, *args, **kwargs):
        page = Pages.objects.get(id=self.kwargs['id'])
        if request.POST.get("title"):
            page.title = request.POST.get("title")
        if request.POST.get("content"):
            page.content = request.POST.get("content")
        page.save()
        messages.success(request, 'Page updated successfully!')
        return redirect('static_pages:view_page',id=page.id)


class DeletePage(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        Pages.objects.get(id=self.kwargs['id']).delete()
        messages.success(request, 'Page deleted successfully!')
        return redirect('static_pages:pages_list')


class ChangePageStatus(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        page = Pages.objects.get(id=self.kwargs['id'])
        if page.is_active:
            page.is_active = False
            message = "page Deactivated Successfully!"
        else:
            page.is_active = True
            message = "Page Activated Successfully!"
        page.save()
        messages.success(request,message)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


"""
Faq Management
"""
class FaqsList(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        faqs = FAQs.objects.all().order_by('-created_on').only('id')
        faqs = query_filter_constructer(
            request, faqs,
            {
                "question__icontains": "question",
                "answer__icontains": "answer",
                "created_on__date": "created_on",
            })

        if not faqs and request.GET:
            messages.error(request, 'No Data Found')
        return render(request,'faq/faq-list.html',{
            'head_title':'FAQs Management',
            "faqs":get_pagination(request, faqs),
            "search_filters":request.GET.copy(),
            "total_objects": faqs.count(),
        })


class ViewFAQ(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        faq = FAQs.objects.get(id=self.kwargs['id'])
        return render(request,'faq/view-faq.html',{'head_title':'FAQs Management','faq':faq})


class AddFAQ(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        return render(request, 'faq/add-faq.html',{"head_title":"FAQs Management"})
    @method_decorator(admin_only)
    def post(self, request, *args, **kwargs):
        question = request.POST.get('question')
        answer = request.POST.get("answer")

        if FAQs.objects.filter(question=question):
            messages.error(request,'FAQ Already Exists!')
            return render(
                request, 'faq/add-faq.html',{
                    "question": question, "answer": answer,
                    "head_title":"FAQs Management"})

        faq = FAQs.objects.create(question=question, answer=answer)
        messages.success(request, 'Faq added successfully!')
        return redirect('static_pages:view_faq',id=faq.id)


class UpdateFAQ(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        faq = FAQs.objects.get(id=self.kwargs['id'])
        return render(request, 'faq/edit-faq.html',{"head_title":"FAQs Management","faq":faq})
    @method_decorator(admin_only)
    def post(self, request, *args, **kwargs):
        faq = FAQs.objects.get(id=self.kwargs['id'])
        if request.POST.get('question'):
            faq.question=request.POST.get('question')
        if request.POST.get('answer'):
            faq.answer = request.POST.get('answer')
        faq.save()
        messages.success(request, 'FAQ updated successfully!')
        return redirect('static_pages:view_faq',id=faq.id)


class DeleteFAQ(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        FAQs.objects.get(id=self.kwargs['id']).delete()
        messages.success(request,'FAQ Deleted Successfully!')
        return redirect('static_pages:faq_list')





"""
Testimonials Sections
"""
class AllTestimonials(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        testimonials = Testimonials.objects.all().order_by('-created_on')
        testimonials = query_filter_constructer(request,testimonials,
            {
                "client_name__icontains":"client_name",
                "client_location__icontains":"client_location",
                "publish_status":"publish_status",
                "created_on__date":"created_on",
            }
        )
        if request.GET and not testimonials:
            messages.error(request, 'No data found!')

        return render(request, 'testimonials/testimonials.html',{
            "testimonials":get_pagination(request,testimonials),
            "head_title":"Testimonials Management",
            "search_filters":request.GET.copy(),
            "total_objects":testimonials.count()
            
        })
    

class ViewTestimonial(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        testimonial = Testimonials.objects.get(id=self.kwargs['id'])
        return render(request, 'testimonials/view-testimonial.html',{
            "testimonial":testimonial,
            "head_title":"Testimonials Management",
        })


class AddTestimonial(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        return render(request, 'testimonials/add-testimonials.html',{
            "head_title":"Testimonials Management",
        })
    @method_decorator(admin_only)
    def post(self, request, *args, **kwargs):
        client_name = request.POST.get('client_name').strip()
        client_location = request.POST.get('client_location').strip()
        if Testimonials.objects.filter(client_name=client_name,client_location=client_location).exists():
            messages.error(request,'Testimonial already exists with this name')
            return redirect('static_pages:add_testimonial')
        
        testimonial = Testimonials.objects.create(
            client_name = client_name,
            client_location = client_location,
            description = request.POST.get('content'),
            client_image = request.FILES.get('client_image',None)
        )
        messages.success(request,'Testimonial added successfully')
        return redirect('static_pages:view_testimonial',id=testimonial.id)


class UpdateTestimonial(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        testimonial = Testimonials.objects.get(id=self.kwargs['id'])
        return render(request, 'testimonials/update-testimonial.html',{
            "head_title":"Testimonials Management",
            "testimonial":testimonial,
        })
    @method_decorator(admin_only)
    def post(self, request, *args, **kwargs):
        testimonial = Testimonials.objects.get(id=self.kwargs['id'])
        client_name = request.POST.get('client_name').strip()
        client_location = request.POST.get('client_location').strip()
        if Testimonials.objects.filter(client_name=client_name,client_location=client_location).exclude(id=testimonial.id).exists():
            messages.error(request,'Testimonial already exists with this name')
            return redirect('static_pages:update_testimonial',id=testimonial.id)
        
        testimonial.client_name = client_name
        testimonial.client_location = client_location
        testimonial.description = request.POST.get('content')
        if request.FILES.get('client_image'):
            testimonial.client_image = request.FILES.get('client_image')
        testimonial.save()
        messages.success(request,'Testimonial updated successfully')
        return redirect('static_pages:view_testimonial',id=testimonial.id)


class PublishUnpublishTestimonial(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        testimonial = Testimonials.objects.get(id=self.kwargs['id'])
        if testimonial.publish_status:
            testimonial.publish_status = False
            messages.success(request,'Testimonial marked as unpublish successfully')
        else:
            ## check for maximum limit of publish testimonials for maximum 5
            if Testimonials.objects.filter(publish_status=True).count() > 4:
                messages.error(request,'Sorry! The maximum limit for published testimonials is 5, so cannot mark this testimonial as published.')
                return redirect('static_pages:view_testimonial',id=testimonial.id)
        
            testimonial.publish_status = True
            testimonial.publish_on = datetime.now()
            messages.success(request,'Testimonial published successfully')
        testimonial.save()
        return redirect('static_pages:view_testimonial',id=testimonial.id)
    

class DeleteTestimonial(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        Testimonials.objects.get(id=self.kwargs['id']).delete()
        messages.success(request,'Testimonial deleted successfully')
        return redirect('static_pages:testimonials')
   

