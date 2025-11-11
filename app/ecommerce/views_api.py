from accounts.common_imports import *
from .serializer import *

class FashionTipsAPI(APIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["Fashion Tips Management"],
        operation_id="Get All Fashion Tips",
        operation_description="Get All Fashion Tips",
        manual_parameters=[
            openapi.Parameter('style', openapi.IN_QUERY, type=openapi.TYPE_STRING, description="Style"),
            openapi.Parameter('season', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="1:Summer, 2:Winter, 3:Rainy, 4:Spring, 5:All Season"),
            openapi.Parameter('gender', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description=" Male:1 Female:2, Other:3 "),
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        ],
    )
    def get(self, request, *args, **kwargs):
        category = request.query_params.get("style")
        season = request.query_params.get("season")
        gender = request.query_params.get("gender")
        category = FashionTipCategory.objects.filter(id = category).first()
        if not category:
            return Response({"message":"Fashion tp category not found ! ","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
       
        fashion_tips = FashionTip.objects.filter(Q(category=category)|Q(season=season)|Q(gender=gender),is_published=True)
        start, end, meta_data = get_pages_data(request.query_params.get('page'), fashion_tips)
        data = FashionTipSerializer(fashion_tips[start:end],many=True,context={"request": request}).data
        return Response({"data": data, "meta": meta_data, "status": status.HTTP_200_OK},status=status.HTTP_200_OK)
