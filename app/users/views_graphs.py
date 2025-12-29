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

        selected_year = int(request.GET.get("year") or datetime.now().year)
        selected_month = request.GET.get("month")

        # Base Query
        base_qs = User.objects.filter(role_id=CUSTOMER, created_on__year=selected_year)

        # Graph structure
        data = {
            "data": [],
            "customers_count": [],
            "active_customers_count": [],
            "inactive_customers_count": [],
            "deleted_customers_count": [],
            "month_name": ""
        }

        def get_counts(qs, extract_type):
            extract = ExtractDay if extract_type == "day" else ExtractMonth

            statuses = {
                "customers_count": qs,
                "active_customers_count": qs.filter(status=ACTIVE),
                "inactive_customers_count": qs.filter(status=INACTIVE),
                "deleted_customers_count": qs.filter(status=DELETED),
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
            for key in ["customers_count", "active_customers_count", "inactive_customers_count", "deleted_customers_count"]:
                data[key] = [counts[key].get(month, 0) for month in months]

        # Chart Y-Axis max
        max_count = max(data["customers_count"] or [0])
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
                {'type': 'spline', 'name': 'Customers Registered', 'data': data['customers_count']},
                {'type': 'column', 'name': 'Active Customers', 'data': data['active_customers_count']},
                {'type': 'column', 'name': 'Inactive Customers', 'data': data['inactive_customers_count']},
                {'type': 'column', 'name': 'Deleted Customers', 'data': data['deleted_customers_count']},
            ]
        }

        return JsonResponse({
            "users": chart,
            "selected_year": selected_year
        })
