import calendar
from accounts.decorators import *
from accounts.utils import *
from django.http import JsonResponse
from accounts.common_imports import *
from django.db.models import Count
from django.db.models.functions import ExtractDay, ExtractMonth


class UserGraph(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):

        data = {
            "data": [],
            'customers_count': [],
            'active_customers_count': [],
            'inactive_customers_count': [],
            'deleted_customers_count': [],
            'month_name': []
        }

        selected_year = int(request.GET.get('year') or datetime.now().year)
        selected_month = request.GET.get('month')
        base_qs = User.objects.filter(role_id=CUSTOMER, created_on__year=selected_year)

        def get_counts(qs, annotate_field):
            counts = {}
            statuses = {
                'customers_count': qs,
                'active_customers_count': qs.filter(status=ACTIVE),
                'inactive_customers_count': qs.filter(status=INACTIVE),
                'deleted_customers_count': qs.filter(status=DELETED),
            }
            extract_func = ExtractDay if annotate_field == 'day' else ExtractMonth

            for key, qs_ in statuses.items():
                annotated = qs_.annotate(**{annotate_field: extract_func('created_on')})
                vals = annotated.values(annotate_field).annotate(count=Count('id')).order_by(annotate_field)
                counts[key] = {item[annotate_field]: item['count'] for item in vals}
            return counts

        if selected_month:
            selected_month = int(selected_month)
            days = range(1, calendar.monthrange(selected_year, selected_month)[1] + 1)
            data['data'] = list(days)
            qs = base_qs.filter(created_on__month=selected_month)
            counts = get_counts(qs, 'day')
            for key in ['customers_count', 'active_customers_count', 'inactive_customers_count', 'deleted_customers_count']:
                data[key] = [counts[key].get(day, 0) for day in days]
            data['month_name'] = calendar.month_name[selected_month]
        else:
            months = range(1, 13)
            data['data'] = [calendar.month_abbr[m] for m in months]
            counts = get_counts(base_qs, 'month')
            for key in ['customers_count', 'active_customers_count', 'inactive_customers_count', 'deleted_customers_count']:
                data[key] = [counts[key].get(month, 0) for month in months]

        max_count = max(data['customers_count'] or [0])
        y_max = 5 if max_count <= 5 else max_count + 10

        chart = {
            'title': {'text': ''},
            'xAxis': {
                'categories': data['data'],
                'lineWidth': 0,
            },
            'yAxis': {
                'min': 0,
                'max': y_max,
                'allowDecimals': False,
                'align': 'left',
                'x': 10,
                'lineWidth': 0,
                'gridLineWidth': 1,
                'title': {'enabled': False},
            },
            'colors': ["#407BFF", "#229b09", "#ffc107", "#e80303"],
            'series': [
                {'type': 'spline', 'name': 'Customers Registered', 'data': data['customers_count']},
                {'type': 'column', 'name': 'Active Customers', 'data': data['active_customers_count']},
                {'type': 'column', 'name': 'Inactive Customers', 'data': data['inactive_customers_count']},
                {'type': 'column', 'name': 'Deleted Customers', 'data': data['deleted_customers_count']},
            ],
            'accessibility': {'enabled': False},
        }

        data['users'] = chart
        data['selected_year'] = selected_year
        return JsonResponse(data)
