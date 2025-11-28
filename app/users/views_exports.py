import csv
import time
import pandas as pd
from accounts.constants import *
from django.http import HttpResponse
from accounts.common_imports import *
from accounts.utils import *


def ConvertDataCSV(data,file_name):
    DATETIME = time.strftime('%Y%m%d-%H%M%S')
    name= file_name + DATETIME
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename= '+ name +".csv"
    writer = csv.writer(response)
    writer.writerow([column for column in data.columns])
    writer.writerows(data.values.tolist())
    return response


'''
Downloads Customer Report
'''

class DownLoadCustomerReports(View):
    @method_decorator(admin_only)
    def post(self, request, *args, **kwargs):
        role_id = int(request.GET.get('role_id'))
        if role_id == 2:
            role = CUSTOMER
            file_name = 'customer_data'
        else:
            role = AFFILIATE   
            file_name = 'affiliate_data'

        users = User.objects.filter(role_id=role).order_by('-created_on')

        if not users:
            messages.success(request, 'No records found.')
            return redirect('users:users_list')

        status_list = []
        for user in users:
            if user.status == ACTIVE:
                status_list.append('Active')
            elif user.status == INACTIVE:
                status_list.append('Inactive')
            elif user.status == DELETED:
                status_list.append('Deleted')
            else:
                status_list.append('--')

        data = pd.DataFrame({
            "Full Name": [user.full_name or '--' for user in users],
            "Email": [user.email or '-' for user in users],
            "Mobile No": [
                f"{user.country_code}{user.mobile_no}" if user.mobile_no else '-'
                for user in users
            ],
            "Created on": [
                convert_to_local_timezone(
                    request.POST.get('timezone'),
                    datetime.strptime(user.created_on.strftime('%Y-%m-%d %H:%M:%S'),
                                      "%Y-%m-%d %H:%M:%S")
                ) if user.created_on else '-'
                for user in users
            ],
            "User Status": status_list,
        })

        return ConvertDataCSV(data, file_name)
