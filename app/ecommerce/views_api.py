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
        manual_parameters=[
            openapi.Parameter('search', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='search by name'),
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        ],
    )
    def get(self, request, *args, **kwargs):
        stores = PartnerStore.objects.all().order_by('-created_on')
        if request.query_params.get('search'):
            stores = PartnerStore.objects.filter(name__icontains = request.query_params.get('search'))
        start, end, meta_data = get_pages_data(request.query_params.get('page'), stores)
        data = PartnerStoresSerializer(stores[start:end],many=True,context={"request": request}).data
        return Response({"data": data, "meta": meta_data, "status": status.HTTP_200_OK},status=status.HTTP_200_OK)
    

class AddRatingAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        tags=['Feedback Management'],
        operation_id="Add Feedback",
        operation_description="Add rating for outfit or wardrobe item",
        manual_parameters=[
            openapi.Parameter('rating', openapi.IN_FORM, type=openapi.TYPE_INTEGER, description='Rate from 1–5'),
            openapi.Parameter('comment', openapi.IN_FORM, type=openapi.TYPE_STRING, description="Feedback comment"),
            openapi.Parameter('item_id', openapi.IN_FORM, type=openapi.TYPE_STRING, description="Wardrobe Item ID"),
            openapi.Parameter('outfit_id', openapi.IN_FORM, type=openapi.TYPE_STRING, description="Outfit ID"),
        ],
    )
    def post(self, request):
        rating_value = request.data.get("rating")
        comment = request.data.get("comment")
        item_id = request.data.get("item_id")
        outfit_id = request.data.get("outfit_id")

        if not item_id and not outfit_id:
            return Response({"error": "Please provide either item_id or outfit_id."},status=status.HTTP_400_BAD_REQUEST)

        if item_id and outfit_id:
            return Response({"error": "Please send only one: item_id OR outfit_id, not both."},status=status.HTTP_400_BAD_REQUEST)

        if not rating_value:
            return Response({"error": "Rating is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            rating_value = int(rating_value)
        except:
            return Response({"error": "Rating must be an integer."}, status=status.HTTP_400_BAD_REQUEST)

        if rating_value < 1 or rating_value > 5:
            return Response({"error": "Rating must be between 1 and 5."}, status=status.HTTP_400_BAD_REQUEST)

        item = None
        outfit = None

        if item_id:
            try:
                item = ClothingItem.objects.get(id=item_id)
            except Exception as e:
                return Response({"error": "Invalid item_id. Item not found."}, status=status.HTTP_404_NOT_FOUND)

        if outfit_id:
            try:
                outfit = Outfit.objects.get(id=outfit_id)
            except Exception as e:
                return Response({"error": "Invalid outfit_id. Outfit not found."}, status=status.HTTP_404_NOT_FOUND)

        rating, created = Rating.objects.update_or_create(
            user=request.user,
            item=item if item else None,
            outfit=outfit if outfit else None,
            defaults={"rating": rating_value, "comment": comment}
        )

        message = "Feedback added successfully!" if created else "Feedback updated successfully!"
        return Response({"message": message,"status":status.HTTP_201_CREATED},status=status.HTTP_201_CREATED)


class FeedbackListAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["Feedback Management"],
        operation_id="Get feedback",
        operation_description="Get feedback",
        manual_parameters=[],
    )
    def get(self, request, *args, **kwargs):
        stores = Rating.objects.all().order_by('-created_on')
        start, end, meta_data = get_pages_data(request.query_params.get('page'), stores)
        data = RatingSerializer(stores[start:end],many=True,context={"request": request}).data
        return Response({"data": data, "meta": meta_data, "status": status.HTTP_200_OK},status=status.HTTP_200_OK)
    

class GetFeedbackDetailsAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["Feedback Management"],
        operation_id="View Feedback Details",
        operation_description="View Feedback Details",
        manual_parameters=[
            openapi.Parameter('feedback_id', openapi.IN_QUERY,type=openapi.TYPE_STRING,description="Feedback Id"),
        ],
    )
    def get(self, request, *args, **kwargs):
        wardrobe = get_or_none(Rating, "Invalid feedback id", id=request.query_params.get('feedback_id'))
        data = RatingSerializer(wardrobe,context = {"request":request}).data
        return Response({"data":data,"status":status.HTTP_200_OK},status=status.HTTP_200_OK)
    