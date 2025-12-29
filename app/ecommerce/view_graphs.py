import calendar
from accounts.decorators import *
from django.http import JsonResponse
from calendar import monthrange
from accounts.common_imports import *
from .models import *
from django.shortcuts import get_object_or_404
from django.db.models.functions import ExtractDay, ExtractMonth


class AffiliateGraph(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        selected_year = int(request.GET.get("year") or datetime.now().year)
        selected_month = request.GET.get("month")
        base_qs = User.objects.filter(role_id=AFFILIATE, created_on__year=selected_year)
        data = {
            "data": [],
            "affiliates_count": [],
            "active_affiliates_count": [],
            "inactive_affiliates_count": [],
            "deleted_affiliates_count": [],
            "month_name": ""
        }

        def get_counts(qs, extract_type):
            extract = ExtractDay if extract_type == "day" else ExtractMonth
            statuses = {
                "affiliates_count": qs,
                "active_affiliates_count": qs.filter(status=ACTIVE),
                "inactive_affiliates_count": qs.filter(status=INACTIVE),
                "deleted_affiliates_count": qs.filter(status=DELETED),
            }
            counts = {}
            for key, s_qs in statuses.items():
                rows = (
                    s_qs.annotate(val=extract("created_on"))
                    .values("val")
                    .annotate(count=Count("id"))
                    .order_by("val")
                )
                counts[key] = {row["val"]: row["count"] for row in rows}
            return counts

        if selected_month:
            selected_month = int(selected_month)

            total_days = calendar.monthrange(selected_year, selected_month)[1]
            days = range(1, total_days + 1)

            data["data"] = list(days)
            data["month_name"] = calendar.month_name[selected_month]

            qs = base_qs.filter(created_on__month=selected_month)

            counts = get_counts(qs, "day")

            for key in data.keys():
                if isinstance(data[key], list):
                    data[key] = [counts[key].get(day, 0) for day in days]

        else:
            months = range(1, 13)
            data["data"] = [calendar.month_abbr[m] for m in months]

            counts = get_counts(base_qs, "month")

            for key in ["affiliates_count", "active_affiliates_count", "inactive_affiliates_count", "deleted_affiliates_count"]:
                data[key] = [counts[key].get(month, 0) for month in months]

        # Chart Y-Axis max
        max_count = max(data["affiliates_count"] or [0])
        y_max = max(max_count + 10, 5)

        chart = {
            'title': {'text': ''},
            'xAxis': {'categories': data['data'], 'lineWidth': 0},
            'yAxis': {
                'min': 0, 'max': y_max, 'allowDecimals': False,
                'title': {'enabled': False},
                'lineWidth': 0, 'gridLineWidth': 1
            },
            'colors': ["#407BFF", "#229b09", "#ffc107", "#e80303"],
            'series': [
                {'type': 'spline', 'name': 'Affiliates Registered', 'data': data['affiliates_count']},
                {'type': 'column', 'name': 'Active Affiliates', 'data': data['active_affiliates_count']},
                {'type': 'column', 'name': 'Inactive Affiliates', 'data': data['inactive_affiliates_count']},
                {'type': 'column', 'name': 'Deleted Affiliates', 'data': data['deleted_affiliates_count']},
            ]
        }

        return JsonResponse({
            "users": chart,
            "selected_year": selected_year
        })


class AffiliatePerformanceGraph(View):
    def get(self, request, *args, **kwargs):
        data = {"data":[],'Orders_count':[],'total_commissions':[],'total_sales':[],'clicks':[],'month_name':[]}
        selected_year = int(request.GET.get("year") or datetime.now().year)
        selected_month = request.GET.get("month")
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