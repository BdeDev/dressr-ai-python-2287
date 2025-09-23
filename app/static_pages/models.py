from django.utils.html import strip_tags
from ckeditor_uploader.fields import RichTextUploadingField
from accounts.models import *
from accounts.constants import *

class Pages(CommonInfo):
    title = models.CharField(max_length=255,blank=True, null=True)
    content = RichTextUploadingField()
    type_id = models.PositiveIntegerField(choices=PAGE_TYPE)
    is_active = models.BooleanField(default=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['content'] = strip_tags(instance.content)
        return data

    class Meta:
        db_table = 'static_pages'
        

class FAQs(CommonInfo):
    question = models.CharField(max_length=255,null=True,blank=True)
    answer = models.TextField(null=True,blank=True)

    class Meta:
        db_table = 'faqs'
        

class Testimonials(CommonInfo):
    client_name = models.CharField(null=True, blank=True,max_length=255)
    client_image = models.FileField(upload_to='testimonials_image/', blank=True, null=True)
    client_location = models.CharField(null=True, blank=True,max_length=255)
    description = models.TextField(null=True, blank=True)
    publish_status = models.BooleanField(default = False)
    publish_on = models.DateTimeField(auto_now=False,null=True,blank=True)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'testimonials'
        