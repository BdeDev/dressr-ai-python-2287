from accounts.utils import get_pagination
from .models import *
from accounts.common_imports import *
import time


"""
Back Up Management
"""
class BackupsList(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        records = Backup.objects.all().order_by('-created_on').only('id')
        records = query_filter_constructer(
            request, records,
            {
                "name__icontains": "name",
                "is_schema": "database_type",
                "created_on__date": "created_on",
            })

        if not records and request.GET:
            messages.error(request, 'No Data Found')
        return render(request, 'backup/backup.html',{
            "head_title": "Backup Management",
            "records": get_pagination(request, records),
            "search_filters":request.GET.copy(),
            "total_objects": records.count(),
        })


class CreateDBBackup(View):
	@method_decorator(admin_only)
	def get(self, request, *args, **kwargs):
		database = env('DB_NAME')
		backup_dir = os.path.join(
			os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'media', 'backup_files'
                  )

		os.makedirs(backup_dir, exist_ok=True)

		filename = f"{database}{time.strftime('%Y%m%d-%H%M%S')}.sql"
		file_path = os.path.join(backup_dir, filename)

		os.system("mysqldump -h " + env('DB_HOST') + " -u " + env('DB_USER') + " -p" + env('DB_PASSWORD') + " " + database + " > " + file_path)

		Backup.objects.create(name=filename, size=os.path.getsize(file_path), is_schema=False, backup_file=f'backup_files/{filename}')

		messages.success(request, 'Database backup created successfully!')
		return redirect('backup:backup')


class CreateDBSchema(View):
	@method_decorator(admin_only)
	def get(self, request, *args, **kwargs):
		database = env('DB_NAME')
		backup_dir = os.path.join(settings.MEDIA_ROOT, 'backup_files')
		os.makedirs(backup_dir, exist_ok=True)

		filename = f"{database}{time.strftime('%Y%m%d-%H%M%S')}.json"
		file_path = os.path.join(backup_dir, filename)

		os.system("mysqldump -h " + env('DB_HOST') + " -u " + env('DB_USER') + " -p" + env('DB_PASSWORD') + " --no-data " + database + " > " + file_path)

		Backup.objects.create(name=filename, size=os.path.getsize(file_path), is_schema=True, backup_file=f'backup_files/{filename}')

		messages.success(request, 'Database structure created successfully!')
		return redirect('backup:backup')


class DeleteBackup(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        Backup.objects.get(id=self.kwargs['id']).delete()
        messages.success(request, 'File deleted successfully!')
        return redirect('backup:backup')
