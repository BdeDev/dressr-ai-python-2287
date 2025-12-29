from django import template
from accounts.views import *
from contact_us.models import *
from wardrobe.models import Wardrobe,VirtualTryOn
from subscription.models import *
from django.http.request import HttpRequest
from django.contrib.sites.shortcuts import get_current_site
import environ

register = template.Library()
env = environ.Env()
environ.Env.read_env()

@register.simple_tag
def protocol_domain(request:HttpRequest):
	current_site = get_current_site(request)
	context = {
            'domain':current_site.domain,
            'protocol': 'https' if USE_HTTPS else 'http',
        }
	return context 

@register.simple_tag
def split_email(email:str):
	return email.split("@")[0]

@register.simple_tag
def url_replace(request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()
	
@register.filter(name='total_customers')
def total_customers(key):
	return User.objects.filter(role_id__in=[CUSTOMER] ).count()

@register.filter(name='notifications_list')
def notifications_list(key):
	admin = User.objects.get(is_superuser=True, role_id=ADMIN)
	return Notifications.objects.filter(created_for=admin, is_read=False).order_by('-created_on')

@register.filter(name="unread_notifications_count")
def unread_notifications_count(request):
	if 'n_id' in request.GET.keys():
		try:
			Notifications.objects.filter(id=request.GET['n_id']).update(is_read=True)
		except:
			pass
	# admin = User.objects.get(is_superuser=True, role_id=ADMIN)
	return Notifications.objects.filter(created_for=request.user, is_read=False).count()

@register.filter(name='convert_local_timezone')
def convert_local_timezone(data,timezone):
	try:
		data = datetime.strptime(data.strftime("%m/%d/%Y, %H:%M:%S"), '%m/%d/%Y, %H:%M:%S')
		local_tz = pytz.timezone('UTC')
		UTC_tz = pytz.timezone(timezone)
		date=datetime.strptime(str(UTC_tz.normalize(local_tz.localize(data).astimezone(UTC_tz))).split("+")[0], "%Y-%m-%d %H:%M:%S")
		return date.strftime("%I:%M %p")

	except Exception as e:
		return None

@register.filter(name='convert_local_timezone_date')
def convert_local_timezone_date(data,timezone):
	try:
		data = datetime.strptime(data.strftime("%m/%d/%Y, %H:%M:%S"), '%m/%d/%Y, %H:%M:%S')
		local_tz = pytz.timezone('UTC')
		UTC_tz = pytz.timezone(timezone)
		date=datetime.strptime(str(UTC_tz.normalize(local_tz.localize(data).astimezone(UTC_tz))).split("+")[0], "%Y-%m-%d %H:%M:%S")
		return date.strftime("%A %d %B, %Y")

	except Exception as e:
		return None

@register.filter(name='today_customers')
def today_customers(key):
	return User.objects.filter(created_on__date=datetime.now().date(),role_id=CUSTOMER).order_by("-created_on")[0:5]

#Dashboard template tags start
@register.filter(name='users_count')
def users_count(key):
	count=0
	if key=='active_user':
		count=User.objects.filter(role_id__in=[CUSTOMER],status=ACTIVE).count()
	elif key=='inactive_user':
		count=User.objects.filter(role_id__in=[CUSTOMER],status=INACTIVE).count()
	elif key=='deleted_user':
		count=User.objects.filter(role_id__in=[CUSTOMER],status=DELETED).count()
	elif key=='total_user':
		count=User.objects.filter(role_id__in=[CUSTOMER]).count()
	return count


@register.filter(name='affiliates_count')
def affiliates_count(key):
	count=0
	if key=='active_affiliate':
		count=User.objects.filter(role_id__in=[AFFILIATE],status=ACTIVE).count()
	elif key=='inactive_affiliate':
		count=User.objects.filter(role_id__in=[AFFILIATE],status=INACTIVE).count()
	elif key=='deleted_affiliate':
		count=User.objects.filter(role_id__in=[AFFILIATE],status=DELETED).count()
	elif key=='total_affiliate':
		count=User.objects.filter(role_id__in=[AFFILIATE]).count()
	return count

@register.filter(name='wardrobe_count')
def wardrobe_count(key):
	if key == 'total_count':
		user_wardrobe = Wardrobe.objects.all().count()
		return user_wardrobe
	return 0


@register.filter(name='contact_us_count')
def contact_us_count(key):
	contact_us_count = ContactUs.objects.all().count()	
	return contact_us_count

@register.filter(name='dashboard_data')
def dashboard_data(key):
	if key == "customers_today":
		return User.objects.filter(created_on__date=datetime.now().date()).exclude(role_id=ADMIN)[0:3]
	if key == "card_today":
		return 0


@register.filter(name='today_date')
def today_date(key):
	return datetime.now()


@register.simple_tag
def date_format(key):
	date= str(key)
	return datetime.strptime(date, '%Y-%m-%d')

@register.filter(name='notifications')
def notifications(user):
	return Notifications.objects.filter(created_for=user,is_read=False).order_by('-created_on')[0:5]

@register.filter(name='notification_count')
def notification_count(user):
	return Notifications.objects.filter(created_for=user,is_read=False).count()

@register.filter(name='unread_notifications')
def unread_notifications(key):
	return Notifications.objects.filter(created_for_id=key).order_by('-id')[0:5]

@register.filter(name='get_extension')
def get_extension(file):
	name, extension = os.path.splitext(file.name)
	if extension.lower() in [".png", '.jpg', '.jpeg','.avif','.webp','.gif']:
		return 'img'
	elif extension.lower() in [".mp4",".mov",".mkv",".3gp"]:
		return 'vid'
	else:
		return 'file'
	
@register.filter(name='filename')
def filename(file):
	return file.name.split("/")[1]


@register.simple_tag(name='convert_into_local_time')
def convert_into_local_time(timezone, created_on, time_format):
    if not created_on:
        return ''
    local_tz = pytz.timezone(timezone)
    local_time = created_on.astimezone(local_tz)
    return local_time.strftime(time_format)


@register.filter(name='convert_to_list')
def convert_to_list(numbers):
	data = [int(i) for i in numbers]
	return data 

@register.simple_tag
def is_favourite(user, item):
    if user.is_authenticated:
        return user.favourite_item.filter(id=item.id).exists()
    return False


@register.filter(name='total_try_on')
def total_try_on(key):
	return VirtualTryOn.objects.all().count()

#Dashboard template tags start
@register.filter(name='subscribers_count')
def subscribers_count(key):
	count=0
	if key=='free_subscribers':
		count=UserPlanPurchased.objects.filter(subscription_plan__is_free_plan=True).count()
	elif key=='premium_subscribers':
		count=UserPlanPurchased.objects.filter(subscription_plan__is_free_plan=False).count()
	elif key=='total_subscribers':
		count=UserPlanPurchased.objects.filter().count()
	return count