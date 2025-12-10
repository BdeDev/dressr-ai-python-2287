import csv
import time
import pandas as pd
from accounts.constants import *
from django.http import HttpResponse
from accounts.common_imports import *
from .models import *
from accounts.utils import *

import calendar
from datetime import datetime
from calendar import monthrange

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
class DownLoadCommissionReport(View):
    @method_decorator(admin_only)
    def post(self, request, *args, **kwargs):
        file_name='affiliate_orders'

        commission_history=CommissionHistory.objects.filter(affiliate=request.user).order_by('-created_on')
        status =[]
        for history in commission_history:
            if history.status == COMMISSION_STATUS_PENDING:
                status.append('Active')
            elif history.status == COMMISSION_STATUS_APPROVED:
                status.append('Inactive')
            elif history.status == COMMISSION_STATUS_PAID:
                status.append('Deleted')
            else:
                status.append('--')
        data = pd.DataFrame({
            "Created At": [convert_to_local_timezone(request.POST.get('timezone'),datetime.strptime(history.created_on.strftime('%Y-%m-%d %H:%M:%S'),"%Y-%m-%d %H:%M:%S")) if history.created_on else '-' for history in commission_history],
            "Referral ID": [history.referral_code if history.referral_code else '-' for history in commission_history],
            "Order Number": [history.transaction.order.order_id if history.transaction.order else '-' for history in commission_history],
            "Sales": [history.transaction.amount if history.transaction.amount else '-' for history in commission_history],
            "Quantity": [len(history.transaction.order.esim_orders.all()) if history.transaction.order.esim_orders else '-' for history in commission_history],
            "Commission": [history.commission_amount if history.commission_amount else '-' for history in commission_history],
            "Status": status
        })
        if not commission_history:
            messages.success(request,'Not Enough Commissions')
            return redirect('affiliate_v2:affiliate_commission')
        return ConvertDataCSV(data,file_name)


"""
Affiliate Performance Report
"""
class DownloadAffiliatePerformanceReport(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        file_name = 'performance_report.csv'
        month = request.GET.get('month')
        year = int(request.GET.get('year', datetime.now().year))
        user = request.user

        # Dynamically set filename
        if month and year:
            month_name = calendar.month_name[int(month)].lower()
            file_name = f"performance_report_{month_name}_{year}.csv"
        else:
            file_name = f"performance_report_{year}.csv"

        # Prepare response as CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'

        writer = csv.writer(response)

        # Header row
        if month:
            writer.writerow(['Date', 'Orders', 'Commissions', 'Sales', 'Clicks'])
            days = [i for i in range(1, monthrange(year, int(month))[1] + 1)]
            for day in days:
                orders = CommissionHistory.objects.filter(
                    affiliate__role_id=AFFILIATE,
                    affiliate=user,
                    created_on__year=year,
                    created_on__month=month,
                    created_on__day=day
                ).count()

                commissions = CommissionHistory.objects.filter(
                    affiliate__role_id=AFFILIATE,
                    affiliate=user,
                    created_on__year=year,
                    created_on__month=month,
                    created_on__day=day
                ).aggregate(Sum("commission_amount", default=0))['commission_amount__sum'] or 0

                sales = CommissionHistory.objects.filter(
                    affiliate__role_id=AFFILIATE,
                    affiliate=user,
                    created_on__year=year,
                    created_on__month=month,
                    created_on__day=day
                ).aggregate(Sum("transaction__amount", default=0))['transaction__amount__sum'] or 0

                clicks = AffiliateClicks.objects.filter(
                    affiliate__role_id=AFFILIATE,
                    affiliate=user,
                    created_on__year=year,
                    created_on__month=month,
                    created_on__day=day
                ).count()

                date_label = f"{day} {calendar.month_name[int(month)]} {year}"
                writer.writerow([date_label, orders, round(commissions, 2), round(sales, 2), clicks])

        else:
            writer.writerow(['Month', 'Orders', 'Commissions', 'Sales', 'Clicks'])
            for i in range(1, 13):
                orders = CommissionHistory.objects.filter(
                    affiliate__role_id=AFFILIATE,
                    affiliate=user,
                    created_on__year=year,
                    created_on__month=i
                ).count()

                commissions = CommissionHistory.objects.filter(
                    affiliate__role_id=AFFILIATE,
                    affiliate=user,
                    created_on__year=year,
                    created_on__month=i
                ).aggregate(Sum("commission_amount", default=0))['commission_amount__sum'] or 0

                sales = CommissionHistory.objects.filter(
                    affiliate__role_id=AFFILIATE,
                    affiliate=user,
                    created_on__year=year,
                    created_on__month=i
                ).aggregate(Sum("transaction__amount", default=0))['transaction__amount__sum'] or 0

                clicks = AffiliateClicks.objects.filter(
                    affiliate__role_id=AFFILIATE,
                    affiliate=user,
                    created_on__year=year,
                    created_on__month=i
                ).count()

                month_label = calendar.month_name[i]
                writer.writerow([month_label, orders, round(commissions, 2), round(sales, 2), clicks])

        return response