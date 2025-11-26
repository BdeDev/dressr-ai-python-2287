import calendar
from accounts.decorators import *
from django.http import JsonResponse
from calendar import monthrange
from accounts.common_imports import *
from .models import *
from django.shortcuts import get_object_or_404

class AffiliatePerformanceGraph(View):
    def get(self, request, *args, **kwargs):
        data = {"data":[],'Orders_count':[],'total_commissions':[],'total_sales':[],'clicks':[],'month_name':[]}
        selected_year = request.GET.get('year') if request.GET.get('year') else datetime.now().year
        selected_month = request.GET.get('month') if request.GET.get('month') else None
        user_id = request.GET.get("user") or self.kwargs.get("id")
        user = get_object_or_404(User, id=user_id)
        if selected_month:
            days = [i for i in range(1,monthrange(int(selected_year), int(selected_month))[1]+1)]
            data['data'] = [day for day in days]
            data['Orders_count']= [CommissionHistory.objects.filter(affiliate__role_id=AFFILIATE,affiliate=user,created_on__month = selected_month,created_on__day = day,created_on__year = selected_year).count() for day in days]
            data['total_commissions']=  [round(CommissionHistory.objects.filter(affiliate__role_id=AFFILIATE,affiliate=user,created_on__month = selected_month,created_on__day = day,created_on__year = selected_year).aggregate(Sum("commission_amount", default=0))['commission_amount__sum'],2) for day in days  ]
            data['total_sales']=  [round(CommissionHistory.objects.filter(affiliate__role_id=AFFILIATE,affiliate=user,created_on__month = selected_month,created_on__day = day,created_on__year = selected_year).aggregate(Sum("transaction__amount", default=0))['transaction__amount__sum'],2) for day in days  ]
            data['clicks']= [AffiliateClicks.objects.filter(affiliate__role_id=AFFILIATE,affiliate=user,created_on__month = selected_month,created_on__day = day,created_on__year = selected_year).count() for day in days  ]
            data['month_name']=calendar.month_name[int(selected_month)]   
        else:
            data['data'] = ['Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            data['Orders_count']= [CommissionHistory.objects.filter(affiliate__role_id=AFFILIATE,affiliate=user,created_on__month=i,created_on__year=selected_year).count() for i in range(1,13)]
            data['total_commissions'] = [round(CommissionHistory.objects.filter(affiliate__role_id=AFFILIATE,affiliate=user,created_on__month=i,created_on__year=selected_year).aggregate(Sum("commission_amount", default=0))['commission_amount__sum'],2) for i in range(1,13)]
            data['total_sales'] = [round(CommissionHistory.objects.filter(affiliate__role_id=AFFILIATE,affiliate=user,created_on__month=i,created_on__year=selected_year).aggregate(Sum("transaction__amount", default=0))['transaction__amount__sum'],2) for i in range(1,13)]
            data['clicks'] = [AffiliateClicks.objects.filter(affiliate__role_id=AFFILIATE,affiliate=user,created_on__month=i,created_on__year=selected_year).count() for i in range(1,13)]

        # Total eSIM count for the selected month
        total_Orders = sum(data['Orders_count'])
        total_commissions = sum(data['total_commissions'])
        total_sales = sum(data['total_sales'])
        total_clicks = sum(data['clicks'])

        # Create a dictionary of all totals
        totals = {
            'Orders': data['Orders_count'],
            'Commissions': data['total_commissions'],
            'Sales': data['total_sales'],
            'Clicks': data['clicks'],
        }

        # Find the metric(s) with the maximum value
        max_value = max(totals.values())
        max_metrics = [key for key, value in totals.items() if value == max_value]


        chart = {
            'title': {
                'text': ''
            },
            'xAxis': { 
                'categories': data['data'],
                'lineWidth': 0,
            },
            'yAxis': {
                'min': 0,
                'max': 5 if max(max_value) <= 5 else max(max_value)+5,
                'allowDecimals': False,
                'align': 'left',
                'x': 10,
                'lineWidth': 0,
                'gridLineWidth': 1,
                'title': {
                    'enabled': False,
                },
            },    
            'colors': ["#407BFF","#229b09","#ffc107","#e27521"],
            'series': [
                {
                    'type': 'spline',
                    'name': 'Orders',
                    'data': data['Orders_count'],
                }, 
                {
                    'type': 'column',
                    'name': 'Commissions',
                    'data': data['total_commissions'],
                }, 
                {
                    'type': 'column',
                    'name': 'Sales',
                    'data': data['total_sales'],
                }, 
                {
                    'type': 'column',
                    'name': 'Clicks',
                    'data': data['clicks'],
                }, 
              
            ],
            'accessibility': {
                'enabled': False
            },
        }

        data['users']=chart   
        data['selected_year']=selected_year
        data['total_Orders']=total_Orders
        data['total_commissions']=round(total_commissions,2)
        data['total_sales']=round(total_sales,2)
        data['total_clicks']=total_clicks
        return JsonResponse(data)