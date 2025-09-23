from accounts.common_imports import *
from static_pages.models import *
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
