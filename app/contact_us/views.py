from .models import *
from accounts.views import *


class ContactUsList(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        contacts = ContactUs.objects.all().order_by('-created_on')
        contacts = query_filter_constructer(
            request, contacts,
            {
                "full_name__icontains": "full_name",
                "is_replied": "is_replied",
                "email__icontains": "email",
                "message__icontains": "message",
                "created_on__date": "created_on",
            })

        if not contacts and request.GET:
            messages.error(request, 'No Data Found')
            
        return render(request, 'contactus/contactus-list.html',{
            "head_title": "Contact Us Management",
            "contacts": get_pagination(request, contacts),
            "total_objects": contacts.count(),
        })


class ViewContactUsDetails(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        contact = ContactUs.objects.get(id=self.kwargs['id'])
        replies = ContactUsReply.objects.filter(contact=contact).order_by('-created_on')
        return render(request, 'contactus/view-contactus.html', {
            "head_title": "Contact Us Management", 
            "contact": contact, 
            "replies": replies
        })


class ContactUsReplyView(View):
    @method_decorator(admin_only)
    def post(self, request, *args, **kwargs):
        contact = ContactUs.objects.get(id=request.POST.get('id'))
        reply = ContactUsReply.objects.create(
            contact = contact,
            reply_message = request.POST.get('reply_message'),
            created_by = request.user
        )
        contact.is_replied = True
        contact.save()
        bulk_send_user_email(request, None, 'EmailTemplates/contactus-reply.html', 'Contact Us Revert', contact.email, contact.message, reply.reply_message, 'Contact Us Revert', '', temp=False)
        messages.success(request,"Reply sent successfully!")
        return redirect('contact_us:view_contact',id=contact.id)


class DeleteContactUs(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        ContactUs.objects.get(id=self.kwargs['id']).delete()
        messages.success(request, "Contact Deleted Successfully!")
        return redirect('contact_us:contactus_list')


"""
Social Links Management
"""
class SocialLinksView(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        social_link = SocialLinks.objects.first()
        if not social_link:
            social_link = SocialLinks.objects.create(created_by=request.user)
        return render(request, 'help-support/social-links.html',{
            "head_title":"Social Links Management",
            "social_link":social_link,
        })
    
    @method_decorator(admin_only)
    def post(self, request, *args, **kwargs):
        social_link = SocialLinks.objects.first()
        if not social_link:
            social_link = SocialLinks.objects.create(created_by=request.user)
        
        social_link.instagram= request.POST.get('instagram',None)
        social_link.facebook= request.POST.get('facebook',None)
        social_link.twitter= request.POST.get('twitter',None)
        social_link.save()
        messages.success(request,'Social link updated successfully')
        return redirect('contact_us:social_links')
   
