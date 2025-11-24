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
            openapi.Parameter('style', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="1:Casual, 2:Formal, 3:Party, 4:Street Style, 5:Classic"),
            openapi.Parameter('season', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="1:Summer, 2:Winter, 3:Rainy, 4:Spring, 5:All Season"),
            openapi.Parameter('gender', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="Male:1 Female:2, Other:3"),
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        ],
    )
    def get(self, request, *args, **kwargs):
        style = request.query_params.get("style")
        season = request.query_params.get("season")
        gender = request.query_params.get("gender")
        fashion_tips = FashionTip.objects.filter(is_published=True)

        if style:
            if int(style) not in [1,2,3,4,5]:
                return Response({"message": "Please enter valid data !", "status": status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
            fashion_tips = fashion_tips.filter(style=style)

        if season:
            if int(season) not in [1,2,3,4,5]:
                return Response({"message": "Please enter valid data !", "status": status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
            fashion_tips = fashion_tips.filter(season=season)

        if gender:
            if int(gender) not in [1,2,3]:
                return Response({"message": "Please enter valid data !", "status": status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
            fashion_tips = fashion_tips.filter(gender=gender)

        # Pagination
        start, end, meta_data = get_pages_data(request.query_params.get("page"), fashion_tips)
        data = FashionTipSerializer(fashion_tips[start:end],many=True,context={"request": request},).data
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