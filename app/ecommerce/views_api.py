from accounts.common_imports import *
from accounts.utils import *
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
       
        fashion_tips = FashionTip.objects.filter(Q(category=category)|Q(season=season)|Q(gender=gender),is_published=True)
        if not fashion_tips:
            fashion_tips = FashionTip.objects.filter(is_published=True)
        start, end, meta_data = get_pages_data(request.query_params.get('page'), fashion_tips)
        data = FashionTipSerializer(fashion_tips[start:end],many=True,context={"request": request}).data
        return Response({"data": data, "meta": meta_data, "status": status.HTTP_200_OK},status=status.HTTP_200_OK)

class BannersListAPI(APIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["Banners Management"],
        operation_id="Get All Banners",
        operation_description="Get All Banners",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        ],
    )
    def get(self, request, *args, **kwargs):
        banners = Banners.objects.filter(is_active = True)
        start, end, meta_data = get_pages_data(request.query_params.get('page'), banners)
        data = BannerSerializer(banners[start:end],many=True,context={"request": request}).data
        return Response({"data": data, "meta": meta_data, "status": status.HTTP_200_OK},status=status.HTTP_200_OK)
    
class PartnerStoresAPI(APIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["Partner Stores Management"],
        operation_id="Get Partner Stores",
        operation_description="Get Partner Stores",
        manual_parameters=[],
    )
    def get(self, request, *args, **kwargs):
        stores = PartnerStore.objects.all().order_by('-created_on')
        start, end, meta_data = get_pages_data(request.query_params.get('page'), stores)
        data = PartnerStoresSerializer(stores[start:end],many=True,context={"request": request}).data
        return Response({"data": data, "meta": meta_data, "status": status.HTTP_200_OK},status=status.HTTP_200_OK)