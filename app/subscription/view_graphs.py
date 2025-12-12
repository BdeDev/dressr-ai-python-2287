import calendar
from accounts.decorators import *
from accounts.utils import *
from django.http import JsonResponse
from accounts.common_imports import *
from django.db.models import Count
from django.db.models.functions import ExtractDay, ExtractMonth


class SubscriberGraph(View):
    @method_decorator(admin_only)
    def get(self, request, *args, **kwargs):
        selected_year = int(request.GET.get("year") or datetime.now().year)
        selected_month = request.GET.get("month")
        base_qs = UserPlanPurchased.objects.filter(created_on__year=selected_year)
        data = {
            "data": [],
            "total_subscribers": [],
            "free_subscribers": [],
            "premium_subscribers": [],
            "month_name": ""
        }

        def get_counts(qs, extract_type):
            extract = ExtractDay if extract_type == "day" else ExtractMonth

            statuses = {
                "total_subscribers": qs,
                "free_subscribers": qs.filter(subscription_plan__is_free_plan=True),
                "premium_subscribers": qs.filter(subscription_plan__is_free_plan=False),
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

            for key in ["total_subscribers", "free_subscribers", "premium_subscribers"]:
                data[key] = [counts[key].get(day, 0) for day in days]

        else:
            months = range(1, 12 + 1)
            data["data"] = [calendar.month_abbr[m] for m in months]

            counts = get_counts(base_qs, "month")

            for key in ["total_subscribers", "free_subscribers", "premium_subscribers"]:
                data[key] = [counts[key].get(month, 0) for month in months]

        max_count = max(data["total_subscribers"] or [0])
        y_max = max(max_count + 10, 5)

        chart = {
            'title': {'text': 'Subscribers Overview'},
            'xAxis': {'categories': data['data'], 'lineWidth': 0},
            'yAxis': {
                'min': 0, 'max': y_max, 'allowDecimals': False,
                'title': {'enabled': False},
                'lineWidth': 0, 'gridLineWidth': 1
            },
            'colors': ["#0d6efd", "#198754", "#ffc107"],
            'series': [
                {'type': 'spline', 'name': 'Total Subscribers', 'data': data['total_subscribers']},
                {'type': 'column', 'name': 'Free Subscribers', 'data': data['free_subscribers']},
                {'type': 'column', 'name': 'Premium Subscribers', 'data': data['premium_subscribers']},
            ]
        }

        return JsonResponse({
            "subscribers": chart,
            "selected_year": selected_year
        })
