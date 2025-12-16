from accounts.common_imports import *
from accounts.utils import *
from .serializer import *
from .healper import *
from accounts.management.commands.default_data import ACTIVITY_ITEM_MAP

class GetWardrobeAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["WarDrobe management"],
        operation_id="wardrobe view",
        operation_description="wardrobe view",
        manual_parameters=[],
    )
    def get(self, request, *args, **kwargs):
        wardrobe = get_or_none(Wardrobe, "Invalid wardrobe id", user=request.user)
        data = WardrobeSerializer(wardrobe,context = {"request":request}).data
        return Response({"data":data,"status":status.HTTP_200_OK},status=status.HTTP_200_OK)

class EditWardrobeAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["WarDrobe management"],
        operation_id="Edit Wardrobe",
        operation_description="Edit Wardrobe",
        manual_parameters=[
            openapi.Parameter('wardrobe_id', openapi.IN_FORM, type=openapi.TYPE_STRING,description='Wardrobe Id'),
            openapi.Parameter('name', openapi.IN_FORM, type=openapi.TYPE_STRING,description='Wardrobe Name'),
        ],
    )
    def post(self, request, *args, **kwargs):
        ## Validate Required Fields
        response = CustomRequiredFieldsValidator.validate_api_field(self, request, [
            {"field_name": "wardrobe_id", "method": "post", "error_message": "Please enter wardrobe id"},
            {"field_name": "name", "method": "post", "error_message": "Please enter wardrobe name"},
        ])
        user = request.user 
        wardrobe = request.data.get('wardrobe_id')  
        if Wardrobe.objects.filter(user=user,name = request.data.get('name').strip()).exclude(id=wardrobe).exists():
            return Response({"message": "Wardrobe already exist with the same name", "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)
        
        wardrobe = get_or_none(Wardrobe, "Invalid wardrobe id", id=request.data.get('wardrobe_id'))
        wardrobe.name = request.data.get('name').strip()
        wardrobe.save()
        data = WardrobeSerializer(wardrobe,context = {"request":request}).data
        return Response({"data":data,"message": "Wardrobe updated successfully!","status":status.HTTP_200_OK},status=status.HTTP_200_OK)

class AddItemInWardrobeAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["WarDrobe management"],
        operation_id="Add Item in Wardrobe",
        operation_description="Add a clothing or accessory item to the user's wardrobe.",
        manual_parameters=[
            openapi.Parameter('title', openapi.IN_FORM, type=openapi.TYPE_STRING, description='title'),
            openapi.Parameter('category_id', openapi.IN_FORM, type=openapi.TYPE_STRING, description='Cloth category ID (e.g., Shirts, Jeans, Shoes)'),
            openapi.Parameter('occasion_id', openapi.IN_FORM, type=openapi.TYPE_STRING, description='Occasion ID'),
            openapi.Parameter('accessory_id', openapi.IN_FORM, type=openapi.TYPE_STRING, description='Accessory ID (e.g., Watch, Bag, Earrings)'),
            openapi.Parameter('weather_type', openapi.IN_FORM, type=openapi.TYPE_STRING, description='1: Summer, 2: Winter, 3: Rainy, 4: Spring, 5: All Season'),
            openapi.Parameter('item_url', openapi.IN_FORM, type=openapi.TYPE_STRING, description='Provide the website link if the item is not available'),
            openapi.Parameter('color', openapi.IN_FORM, type=openapi.TYPE_STRING, description='Color'),
            openapi.Parameter('brand', openapi.IN_FORM, type=openapi.TYPE_STRING, description='Brand'),
            openapi.Parameter('image', openapi.IN_FORM, type=openapi.TYPE_FILE, description='Image file'),
        ],
    )
    def post(self, request, *args, **kwargs):
        user = request.user

        try:
            wardrobe = Wardrobe.objects.get(user=user)
        except Wardrobe.DoesNotExist:
            return Response({"message": "User wardrobe not found. Please create a wardrobe first.","status": status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)

        category = None
        occasion = None
        accessory = None

        if request.data.get('category_id'):
            category = ClothCategory.objects.filter(id=request.data.get('category_id')).first()
            if not category:
                return Response({"message": "Invalid category ID.","status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

        if request.data.get('occasion_id'):
            occasion = Occasion.objects.filter(id=request.data.get('occasion_id')).first()
            if not occasion:
                return Response({"message": "Invalid occasion ID.","status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
            
        if request.data.get('accessory_id'):
            accessory = Accessory.objects.filter(id=request.data.get('accessory_id')).first()
            if not accessory:
                return Response({"message": "Invalid accessory ID.","status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

        if not int(request.data.get('weather_type')) in [1,2,3,4,5]:
            return Response({"message":"Weather type does not matched!", "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        
        cloth_item = ClothingItem.objects.create(
            title = request.data.get('title'),
            wardrobe=wardrobe,
            cloth_category=category,
            occasion=occasion,
            accessory=accessory,
            weather_type=int(request.data.get('weather_type')),
            color=request.data.get('color'),
            brand=request.data.get('brand'),
            date_added=datetime.now(),
            image=request.FILES.get('image')
        )
        if request.data.get('item_url'):
            cloth_item.item_url  = request.data.get('item_url')
        cloth_item.save()

        return Response({"message": "Item added successfully!","status": status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
    

class AddMultipleItemInWardrobeAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["WarDrobe management"],
        operation_id="Add Multiple Item in Wardrobe",
        operation_description="Add Multiple Item in Wardrobe",
        manual_parameters=[
            openapi.Parameter(
                'items',
                openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                description='Example: '
                            '[{"title":"White Shirt","category_id":"...","image_key":0},'
                            '{"title":"Black Jeans","category_id":"...","image_key":1}]'
            ),
            openapi.Parameter('images',openapi.IN_FORM,type=openapi.TYPE_ARRAY,items=openapi.Items(type=openapi.TYPE_FILE),description="Upload images in array order: image[0], image[1], ..."),
        ],
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        wardrobe = get_or_none(Wardrobe, "User wardrobe does not exist !", user=user)
        raw_items = request.data.get("items")
        if not raw_items:
            return Response({"message": "Items list missing!", "status": 400}, status=400)

        try:
            items = json.loads(raw_items)
        except:
            return Response({"message": "Invalid JSON format for items.", "status": 400}, status=400)

        if not isinstance(items, list) or not items:
            return Response({"message": "Items must be a non-empty list.", "status": 400}, status=400)

        incoming_count = len(items)
        wardrobe_item_count = ClothingItem.objects.filter(wardrobe=wardrobe).count()

        # Free plan validation
        purchased_plan = UserPlanPurchased.objects.filter(status=USER_PLAN_ACTIVE,purchased_by=request.user).first()
        if purchased_plan.expire_on <= datetime.now():
            return Response({"message": "Your free plan has expired.", "status": 400}, status=400)

        max_uploads = purchased_plan.subscription_plan.max_uploads
        remaining = max_uploads - wardrobe_item_count

        if remaining <= 0:
            return Response({"message": "Upload limit reached.", "status": 400}, status=400)

        if incoming_count > remaining:
            return Response({"message": f"You can upload only {remaining} items.", "status": 400}, status=400)
      
        created_items = []
        images = request.FILES.getlist("images")

        for idx, item in enumerate(items):
            category = ClothCategory.objects.filter(id=item.get("category_id")).first()
            if not category:
                return Response({"message": "Invalid category ID", "status": 400}, status=400)
            occasion = None
            if item.get("occasion_id"):
                occasion = Occasion.objects.filter(id=item.get("occasion_id")).first()
                if not occasion:
                    return Response({"message": "Invalid occasion ID", "status": 400}, status=400)
                
            accessory = None
            if item.get("accessory_id"):
                accessory = Accessory.objects.filter(id=item.get("accessory_id")).first()
                if not accessory:
                    return Response({"message": "Invalid accessory ID", "status": 400}, status=400)

            if int(item.get("weather_type")) not in [1, 2, 3, 4, 5]:
                return Response({"message": "Invalid weather type", "status": 400}, status=400)

            image_file = None
            image_index = item.get("image_key")
            if image_index is not None:
                try:
                    image_file = images[int(image_index)]
                except:
                    image_file = None
            cloth_item = ClothingItem.objects.create(
                title=item.get("title"),
                wardrobe=wardrobe,
                cloth_category=category,
                occasion=occasion,
                accessory=accessory,
                weather_type=int(item.get("weather_type")),
                color=item.get("color"),
                brand=item.get("brand"),
                image=image_file,
                date_added=datetime.now()
            )

            if item.get("item_url"):
                cloth_item.item_url = item.get("item_url")
            cloth_item.save()
            created_items.append(cloth_item.id)

        return Response({"message": "Items added successfully!","created_item_ids": created_items,"status": 201}, status=201)

class RemoveItemFromWardrobeAPI(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    parser_classes = [MultiPartParser,FormParser]

    @swagger_auto_schema(
        tags=['WarDrobe management'],
        operation_id="Delete Items From wardrobe",
        operation_description="Delete Items From wardrobe",
        manual_parameters=[
            openapi.Parameter('cloth_item_id', openapi.IN_QUERY, type=openapi.TYPE_STRING)
        ],
    )
    def delete(self, request, *args, **kwargs):
        response = CustomRequiredFieldsValidator.validate_api_field(self, request, [
            {"field_name": "cloth_item_id", "method": "get", "error_message": "Please enter cloth item id"},
        ])
        cloth_item = get_or_none(ClothingItem, "Invalid cloth item id", id=request.query_params.get('cloth_item_id'))
        cloth_item.delete()
        return Response({"message":"Coth Item Deleted Successfully!","status": status.HTTP_200_OK}, status = status.HTTP_200_OK)

class RemoveAllItemFromWardrobeAPI(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    parser_classes = [MultiPartParser,FormParser]

    @swagger_auto_schema(
        tags=['WarDrobe management'],
        operation_id="Delete All Items From wardrobe",
        operation_description="Delete All Items From wardrobe",
        manual_parameters=[],
    )
    def delete(self, request, *args, **kwargs):
        wardrobe  = get_or_none(Wardrobe,'Wardrobe does not exist !',user=request.user)
        cloth_item = ClothingItem.objects.filter(wardrobe=wardrobe)
        cloth_item.delete()
        return Response({"message":"Coth Items Deleted Successfully!","status": status.HTTP_200_OK}, status = status.HTTP_200_OK)

class GetItemAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["WarDrobe management"],
        operation_id="Get Cloth Item",
        operation_description="Get Cloth Item",
        manual_parameters=[
            openapi.Parameter('cloth_item_id', openapi.IN_QUERY, type=openapi.TYPE_STRING)
        ],
    )
    def get(self, request, *args, **kwargs):
        response = CustomRequiredFieldsValidator.validate_api_field(self, request, [
            {"field_name": "cloth_item_id", "method": "get", "error_message": "Please enter cloth item id"},
        ])
        cloth_item = get_or_none(ClothingItem, "Invalid cloth item id", id=request.query_params.get('cloth_item_id'))
        data = ClothItemSerializer(cloth_item,context = {"request":request}).data
        return Response({"data":data,"status":status.HTTP_200_OK},status=status.HTTP_200_OK)
    
class GetItemsAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["WarDrobe management"],
        operation_id="Get All Cloth",
        operation_description="Get All Cloth",
        manual_parameters=[],
    )
    def get(self, request, *args, **kwargs):
        # wardrobe = get_or_none(Wardrobe, "Invalid wardrobe id",user=request.user)
        cloth_item = ClothingItem.objects.filter(wardrobe__user = request.user)
        start,end,meta_data = get_pages_data(request.query_params.get('page', None), cloth_item)
        data = ClothItemSerializer(cloth_item[start : end],many=True,context = {"request":request}).data
        return Response({"data":data,"meta":meta_data,"status":status.HTTP_200_OK},status=status.HTTP_200_OK)
    
class EditWardrobeItemAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["WarDrobe management"],
        operation_id="Edit Wardrobe Item api",
        operation_description="Edit Wardrobe Item api",
        manual_parameters=[
            openapi.Parameter('cloth_item_id', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('title', openapi.IN_FORM, type=openapi.TYPE_STRING,description='title'),
            openapi.Parameter('category_id', openapi.IN_FORM, type=openapi.TYPE_STRING,description='category id'),
            openapi.Parameter('occasion_id', openapi.IN_FORM, type=openapi.TYPE_STRING,description='Occasion Id'),
            openapi.Parameter('accessory_id', openapi.IN_FORM, type=openapi.TYPE_STRING,description='Accessory Id'),
            openapi.Parameter('weather_type', openapi.IN_FORM, type=openapi.TYPE_STRING,description='1:Summer , 2:Winter , 3:Rainy , 4:Spring , 5:All Season'),
            openapi.Parameter('color', openapi.IN_FORM, type=openapi.TYPE_STRING,description='Color'),
            openapi.Parameter('brand', openapi.IN_FORM, type=openapi.TYPE_STRING,description='Brand'),
            openapi.Parameter('price', openapi.IN_FORM, type=openapi.TYPE_STRING,description='Price'),
            openapi.Parameter('image', openapi.IN_FORM, type=openapi.TYPE_FILE,description='image'),
        ],
    )
    def post(self, request, *args, **kwargs):
        ## Validate Required Fields
        response = CustomRequiredFieldsValidator.validate_api_field(self, request, [
            {"field_name": "cloth_item_id", "method": "post", "error_message": "Please enter cloth item id"},
        ])
        wardrobe = Wardrobe.objects.get(user=request.user)
        cloth_item = get_or_none(ClothingItem, "Invalid cloth item id", id=request.data.get('cloth_item_id'),wardrobe=wardrobe)
        
        if request.data.get('category_id'):
            category = ClothCategory.objects.get(id = request.data.get('category_id'))
            if not category:
                return Response({"message": "Category does not exist!", "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        if  request.data.get('occasion_id'):
            occasion = Occasion.objects.get(id = request.data.get('occasion_id'))
            if not occasion:
                return Response({"message": "Occasion does not exist!", "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        
        if request.data.get('accessory_id'):
            accessory = Accessory.objects.get(id = request.data.get('accessory_id'))
            if not accessory:
                return Response({"message": "Accessory does not exist!", "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        
        if request.data.get('weather_type'):
            weather_type = int(request.data.get('weather_type'))
            if not int(request.data.get('weather_type')) in [1,2,3,4,5]:
                return Response({"message":"Weather type does not matched!", "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        
        if request.data.get('title'):
            cloth_item.title = request.data.get('title').strip()
        if request.data.get('weather_type'):
            cloth_item.weather_type = weather_type
        if request.data.get('category_id'):
            cloth_item.cloth_category = category
        if request.data.get('accessory_id'):
            cloth_item.accessory = accessory
        if request.data.get('occasion_id'):
            cloth_item.occasion = occasion
        if request.data.get('color'):
            cloth_item.color = request.data.get('color')
        if request.data.get('brand'):
            cloth_item.brand = request.data.get('brand')
        if request.data.get('price'):
            cloth_item.price = request.data.get('price')
        if request.FILES.get('image'):
            cloth_item.image = request.FILES.get('image')
        cloth_item.save()
        data = ClothItemSerializer(cloth_item,context = {"request":request}).data
        return Response({"data":data,"message": "Wardrobe updated successfully!","status":status.HTTP_200_OK},status=status.HTTP_200_OK)

class GetAccessoriesAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["WarDrobe management"],
        operation_id="Get All Accessories",
        operation_description="Get All Accessories",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
        ],
    )
    def get(self, request, *args, **kwargs):
        accessories = Accessory.objects.all().order_by('-created_on')
        start,end,meta_data = get_pages_data(request.query_params.get('page', None), accessories)
        data = AccessorySerializer(accessories[start : end],many=True,context = {"request":request}).data
        return Response({"data":data,"meta":meta_data,"status":status.HTTP_200_OK},status=status.HTTP_200_OK)

class GetOccasionsAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["WarDrobe management"],
        operation_id="Get All Occasions",
        operation_description="Get All Occasions",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
        ],
    )
    def get(self, request, *args, **kwargs):
        occasions = Occasion.objects.all().order_by('-created_on')
        start,end,meta_data = get_pages_data(request.query_params.get('page', None), occasions)
        data = OccasionSerializer(occasions[start : end],many=True,context = {"request":request}).data
        return Response({"data":data,"meta":meta_data,"status":status.HTTP_200_OK},status=status.HTTP_200_OK)
    
class GetClothCategoriesAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["WarDrobe management"],
        operation_id="Cloth Categories",
        operation_description="Get Cloth Categories",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
        ],
    )
    def get(self, request, *args, **kwargs):
        occasions = ClothCategory.objects.all().order_by('-created_on')
        start,end,meta_data = get_pages_data(request.query_params.get('page', None), occasions)
        data = ClothCategorySerializer(occasions[start : end],many=True,context = {"request":request}).data
        return Response({"data":data,"meta":meta_data,"status":status.HTTP_200_OK},status=status.HTTP_200_OK)

####--------------------OutFit Management API's------------------######
class CreateOutfitAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["Outfit Management"],
        operation_id="Create Outfit",
        operation_description="Create Outfit",
        manual_parameters=[
            openapi.Parameter('item_ids', openapi.IN_FORM, type=openapi.TYPE_ARRAY,items=openapi.Items(type=openapi.TYPE_STRING), description='List of Item IDs'),
            openapi.Parameter('occasion_id', openapi.IN_FORM, type=openapi.TYPE_STRING, description='Occasion ID'),
            openapi.Parameter('weather_type', openapi.IN_FORM, type=openapi.TYPE_STRING, description='1:Summer, 2:Winter, 3:Rainy, 4:Spring, 5:All Season'),
            openapi.Parameter('color', openapi.IN_FORM, type=openapi.TYPE_STRING, description='Color'),
            openapi.Parameter('title', openapi.IN_FORM, type=openapi.TYPE_STRING, description='title'),
            openapi.Parameter('image', openapi.IN_FORM, type=openapi.TYPE_FILE, description='outfit image'),
        ],
    )
    def post(self, request):
        user = request.user
        occasion = Occasion.objects.filter(id=request.data.get('occasion_id')).first()
        if not occasion:
            return Response({"message": "Invalid occasion ID.","status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

        if int(request.data.get('weather_type')) not in [1, 2, 3, 4, 5]:
            return Response({"message": "Invalid weather type","status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

        items = ClothingItem.objects.filter(id__in=request.data.getlist('item_ids'),wardrobe__user=user)

        if request.data.get('color'):
            items = items.filter(Q(color__iexact=request.data.get('color')) | Q(color__isnull=True))

        if not items.exists():
            return Response({"message": "No matching clothing items found for the given filters.", "status": status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)

        if Outfit.objects.filter(title=request.data.get('title').strip(),occasion=occasion).exists():
            return Response({"message":"Outfit already exist with title !","status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        
        outfit = Outfit.objects.create(
            title=request.data.get('title').strip(),
            occasion=occasion,
            weather_type=int(request.data.get('weather_type')),
            created_by=user,
            color=request.data.get('color')
        )
        outfit.items.set(items)
        outfit.image = request.FILES.get('image')
        outfit.save()
        return Response({"message": "Outfit created successfully!","outfit_id": outfit.id,"total_items": items.count(),"status": status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)

class MyOutFitListAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["Outfit Management"],
        operation_id="Get All My Outfit",
        operation_description="Get All My Outfit",
        manual_parameters=[
            openapi.Parameter('occasion_id', openapi.IN_QUERY, type=openapi.TYPE_STRING,description='occasion id'),
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        ],
    )
    def get(self, request, *args, **kwargs):
        outfits = Outfit.objects.filter(created_by=request.user).order_by('-created_on')
        if request.query_params.get('occasion_id'):
            outfits = Outfit.objects.filter(occasion=request.query_params.get('occasion_id').strip(),created_by=request.user).order_by('-created_on')

        start,end,meta_data = get_pages_data(request.query_params.get('page', None), outfits)
        data = MyOutFitSerializer(outfits[start : end],many=True,context = {"request":request}).data
        return Response({"data":data,"meta":meta_data,"status":status.HTTP_200_OK},status=status.HTTP_200_OK)
    
class GetMyOutfitAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["Outfit Management"],
        operation_id="Get outfit",
        operation_description="Get outfit",
        manual_parameters=[
            openapi.Parameter('outfit_id', openapi.IN_QUERY, type=openapi.TYPE_STRING)
        ],
    )
    def get(self, request, *args, **kwargs):
        response = CustomRequiredFieldsValidator.validate_api_field(self, request, [
            {"field_name": "outfit_id", "method": "get", "error_message": "Please enter outfit id"},
        ])
        outfit = get_or_none(Outfit, "Invalid outfit id", id=request.query_params.get('outfit_id'))
        data = MyOutFitSerializer(outfit,context = {"request":request}).data
        return Response({"data":data,"status":status.HTTP_200_OK},status=status.HTTP_200_OK)
    
class DeleteOutfitAPI(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    parser_classes = [MultiPartParser,FormParser]

    @swagger_auto_schema(
        tags=['Outfit Management'],
        operation_id="Delete outfit",
        operation_description="Delete outfit",
        manual_parameters=[
            openapi.Parameter('outfit_id', openapi.IN_QUERY, type=openapi.TYPE_STRING)
        ],
    )
    def delete(self, request, *args, **kwargs):
        response = CustomRequiredFieldsValidator.validate_api_field(self, request, [
            {"field_name": "outfit_id", "method": "get", "error_message": "Please enter outfit id"},
        ])
        outfit = get_or_none(Outfit, "Invalid outfit id", id=request.query_params.get('outfit_id').strip())
        outfit.delete()
        return Response({"message":"Outfit Deleted Successfully!","status": status.HTTP_200_OK}, status = status.HTTP_200_OK)

class EditOutfitAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["WarDrobe management"],
        operation_id="Edit Wardrobe",
        operation_description="Edit Wardrobe",
        manual_parameters=[
            openapi.Parameter('outfit_id', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('accessory_ids', openapi.IN_FORM, type=openapi.TYPE_ARRAY,items=openapi.Items(type=openapi.TYPE_STRING), description='List of Accessory IDs'),
            openapi.Parameter('category_ids', openapi.IN_FORM, type=openapi.TYPE_ARRAY,items=openapi.Items(type=openapi.TYPE_STRING), description='List of Category IDs'),
            openapi.Parameter('occasion_id', openapi.IN_FORM, type=openapi.TYPE_STRING, description='Occasion ID'),
            openapi.Parameter('weather_type', openapi.IN_FORM, type=openapi.TYPE_STRING, description='1:Summer, 2:Winter, 3:Rainy, 4:Spring, 5:All Season'),
            openapi.Parameter('color', openapi.IN_FORM, type=openapi.TYPE_STRING, description='Color'),
            openapi.Parameter('title', openapi.IN_FORM, type=openapi.TYPE_STRING, description='Outfit'),
            openapi.Parameter('image', openapi.IN_FORM, type=openapi.TYPE_STRING, description='Outfit Image'),
        ],
    )
    def post(self, request, *args, **kwargs):
        ## Validate Required Fields
        response = CustomRequiredFieldsValidator.validate_api_field(self, request, [
            {"field_name": "outfit_id", "method": "post", "error_message": "Please enter outfit id"},
        ])
        user = request.user 
        outfit = get_or_none(Outfit, "Invalid outfit id", id=request.data.get('outfit_id'),created_by=request.user)

        if request.data.getlist('accessory_ids'):
            valid_accessories = Accessory.objects.filter(id__in=request.data.getlist('accessory_ids')[0].split(','))
           
        if request.data.getlist('category_ids'):
            valid_categories = ClothCategory.objects.filter(id__in=request.data.getlist('category_ids')[0].split(','))

        occasion = Occasion.objects.filter(id=request.data.get('occasion_id')).first()
        if not occasion:
            return Response({"message": "Invalid occasion ID.","status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

        if int(request.data.get('weather_type')) not in [1, 2, 3, 4, 5]:
            return Response({"message": "Invalid weather type","status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        items = ClothingItem.objects.filter(wardrobe__user=user).filter(Q(weather_type=int(request.data.get('weather_type')))|Q(occasion_id=request.data.get('occasion_id')),Q(cloth_category__in = valid_categories)|Q(accessory__in = valid_accessories))
        if request.data.get('color'):
            items = items.filter(Q(color__iexact=request.data.get('color')) | Q(color__isnull=True))
        if not items.exists():
            return Response({"message": "No matching clothing items found for the given filters.", "status": status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)

        if request.data.get('title'):
            outfit.title = request.data.get('title').strip()
        if request.data.get('color'):
            outfit.color = request.data.get('color').strip()
        if request.data.get('occasion_id'):
            occasion = Occasion.objects.filter(id=request.data.get('occasion_id')).first()
            if not occasion:
                return Response({"message": "Invalid occasion ID.","status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
            outfit.occasion = occasion
        if request.data.get('weather_type'):
            outfit.weather_type = int(request.data.get('weather_type'))
        if items:
            outfit.items.set(items)
            outfit.image = request.FILES.get('image')
        outfit.save()
        data = MyOutFitSerializer(outfit,context = {"request":request}).data
        return Response({"data":data,"message": "Outfit updated successfully!","status":status.HTTP_200_OK},status=status.HTTP_200_OK)

class RemoveItemsFromOutfitAPI(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    parser_classes = [MultiPartParser,FormParser]

    @swagger_auto_schema(
        tags=['Outfit Management'],
        operation_id="Delete item from outfit",
        operation_description="Delete item from outfit",
        manual_parameters=[
            openapi.Parameter('outfit_id', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('item_id', openapi.IN_QUERY, type=openapi.TYPE_STRING)
        ],
    )
    def delete(self, request, *args, **kwargs):
        response = CustomRequiredFieldsValidator.validate_api_field(self, request, [
            {"field_name": "outfit_id", "method": "get", "error_message": "Please enter outfit id"},
            {"field_name": "item_id", "method": "get", "error_message": "Please enter item id"},
        ])
        outfit = get_or_none(Outfit, "Invalid outfit id", id=request.query_params.get('outfit_id'))
        if not outfit.items.filter(id=request.query_params.get('item_id')).exists():
            return Response({"error": "Item not found in this outfit"}, status=status.HTTP_404_NOT_FOUND)
        outfit.items.remove(request.query_params.get('item_id'))
        outfit.save()
        return Response({"message":"Outfit Deleted Successfully!","status": status.HTTP_200_OK}, status = status.HTTP_200_OK)

class AddItemInOutfitAPI(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    parser_classes = [MultiPartParser,FormParser]

    @swagger_auto_schema(
        tags=['Outfit Management'],
        operation_id="Add item from outfit",
        operation_description="Add item from outfit",
        manual_parameters=[
            openapi.Parameter('outfit_id', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('item_id', openapi.IN_FORM, type=openapi.TYPE_STRING,description="Item id"),
            openapi.Parameter('image', openapi.IN_FORM, type=openapi.TYPE_FILE,description='Outfit Image'),
        ],
    )
    def post(self, request, *args, **kwargs):
        response = CustomRequiredFieldsValidator.validate_api_field(self, request, [
            {"field_name": "outfit_id", "method": "post", "error_message": "Please enter outfit id"},
            {"field_name": "item_id", "method": "post", "error_message": "Please enter item id"},
        ])
        outfit = get_or_none(Outfit, "Invalid outfit id", id=request.data.get('outfit_id').strip())
        if outfit.items.filter(id=request.data.get('item_id')).exists():
            return Response({"message": "Item already exists in this outfit.", "status": status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        outfit.items.add(request.data.get('item_id').strip())
        outfit.image = request.FILES.get('image')
        outfit.save()
        return Response({"message":"Outfit addedd Successfully!","status": status.HTTP_200_OK}, status = status.HTTP_200_OK)

#####----------------------Trip Management API's--------------------------###

class GetMyAllTripAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["Trip Management"],
        operation_id="Get All My Trips",
        operation_description="Get All My Trips",
        manual_parameters=[
            openapi.Parameter('month', openapi.IN_QUERY, type=openapi.TYPE_STRING,description='YYYY-MM'),
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
        ],
    )
    def get(self, request, *args, **kwargs):
        trips = Trips.objects.filter(created_by = request.user).order_by('-created_on')
        month_param = request.query_params.get("month")
        if month_param:
            try:
                year, month_num = map(int, month_param.split("-"))
                start = date(year, month_num, 1)
                if month_num == 12:
                    end = date(year + 1, 1, 1)
                else:
                    end = date(year, month_num + 1, 1)
                trips = trips.filter(start_date__gte=start, start_date__lt=end)

            except Exception:
                return Response(
                    {"message": "Invalid month format. Use YYYY-MM.", "status": status.HTTP_400_BAD_REQUEST},
                    status=status.HTTP_400_BAD_REQUEST
                )

        start,end,meta_data = get_pages_data(request.query_params.get('page', None), trips,3)
        data = TripsSerializer(trips[start : end],many=True,context = {"request":request}).data
        return Response({"data":data,"meta":meta_data,"status":status.HTTP_200_OK},status=status.HTTP_200_OK)
    
class GetMyTripOutfitsAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["Trip Management"],
        operation_id="Get trip",
        operation_description="Get trip",
        manual_parameters=[
            openapi.Parameter('trip_id', openapi.IN_QUERY, type=openapi.TYPE_STRING)
        ],
    )
    def get(self, request, *args, **kwargs):
        response = CustomRequiredFieldsValidator.validate_api_field(self, request, [
            {"field_name": "trip_id", "method": "get", "error_message": "Please enter trip id"},
        ])
        trip = get_or_none(Trips, "Invalid trip id", id=request.query_params.get('trip_id'))
        data = TripsSerializer(trip,context = {"request":request}).data
        return Response({"data":data,"status":status.HTTP_200_OK},status=status.HTTP_200_OK)
    
class DeleteTripAPI(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    parser_classes = [MultiPartParser,FormParser]

    @swagger_auto_schema(
        tags=['Trip Management'],
        operation_id="Delete trip",
        operation_description="Delete trip",
        manual_parameters=[
            openapi.Parameter('trip', openapi.IN_QUERY, type=openapi.TYPE_STRING),
        ],
    )
    def delete(self, request, *args, **kwargs):
        response = CustomRequiredFieldsValidator.validate_api_field(self, request, [
            {"field_name": "trip", "method": "get", "error_message": "Please enter trip id"},
        ])
        trip = get_or_none(Trips, "Invalid trip id", id=request.query_params.get('trip'))
        trip.delete()
        return Response({"message":"Trip Deleted Successfully!","status": status.HTTP_200_OK}, status = status.HTTP_200_OK)
    
class AddAcivityFlagsAPI(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    parser_classes = [MultiPartParser,FormParser]

    @swagger_auto_schema(
        tags=['Activity Flags Management'],
        operation_id="Add activity flags",
        operation_description="Add activity flags",
        manual_parameters=[
            openapi.Parameter('name', openapi.IN_FORM, type=openapi.TYPE_STRING,description="activity name"),
            openapi.Parameter('description', openapi.IN_FORM, type=openapi.TYPE_STRING,description="activity description"),
            openapi.Parameter('is_other', openapi.IN_FORM, type=openapi.TYPE_STRING,description="if choose other option")
        ],
    )
    def post(self, request, *args, **kwargs):
        response = CustomRequiredFieldsValidator.validate_api_field(self, request, [
            {"field_name": "name", "method": "post", "error_message": "Please enter name"},
            {"field_name": "description", "method": "post", "error_message": "Please enter description"},
        ])
        activity_flags,crested = ActivityFlag.objects.get_or_create(
            name = request.data.get('title').strip(),
            description = request.data.get('description').strip(),
            created_by = request.user
        )
        if crested:
            return Response({"message":"Activity flag already exist !","status": status.HTTP_400_BAD_REQUEST}, status = status.HTTP_400_BAD_REQUEST)
        return Response({"message":"Activity flag created Successfully !","status": status.HTTP_200_OK}, status = status.HTTP_200_OK)
    
class EditAcivityFlagsAPI(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    parser_classes = [MultiPartParser,FormParser]

    @swagger_auto_schema(
        tags=['Activity Flags Management'],
        operation_id="Edit activity flags",
        operation_description="Edit activity flags",
        manual_parameters=[
            openapi.Parameter('activity_flag_id', openapi.IN_FORM, type=openapi.TYPE_STRING,description="activity flag id"),
            openapi.Parameter('name', openapi.IN_FORM, type=openapi.TYPE_STRING,description="activity name"),
            openapi.Parameter('description', openapi.IN_FORM, type=openapi.TYPE_STRING,description="activity description"),
            openapi.Parameter('is_other', openapi.IN_FORM, type=openapi.TYPE_STRING,description="if choose other option")
        ],
    )
    def post(self, request, *args, **kwargs):
        response = CustomRequiredFieldsValidator.validate_api_field(self, request, [
            {"field_name": "activity_flag_id", "method": "post", "error_message": "Please enter activity flag id"},
        ])

        activity_flag = get_or_none(ActivityFlag, "Activity flag does not exist !",id = request.data.get('activity_flag_id'),created_by=request.user)
        if request.data.get('name'):
            activity_flag.name = request.data.get('name')
        if request.data.get('description'):
            activity_flag.description = request.data.get('description')
        activity_flag.save()
        return Response({"message":"Activity flag updated Successfully !","status": status.HTTP_200_OK}, status = status.HTTP_200_OK)

class ActivityFlagListAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["Activity Flags Management"],
        operation_id="Get All activity flags",
        operation_description="Get All activity flags",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
        ],
    )
    def get(self, request, *args, **kwargs):
        activity_flags = ActivityFlag.objects.all().order_by('-created_on')
        start,end,meta_data = get_pages_data(request.query_params.get('page', None), activity_flags)
        data = ActivityFlagSerializer(activity_flags[start : end],many=True,context = {"request":request}).data
        return Response({"data":data,"meta":meta_data,"status":status.HTTP_200_OK},status=status.HTTP_200_OK)
    
class MyActivityFlagListAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["Activity Flags Management"],
        operation_id="My activity flags",
        operation_description="My activity flags",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
        ],
    )
    def get(self, request, *args, **kwargs):
        activity_flags = ActivityFlag.objects.filter(created_by=request.user).order_by('-created_on')
        start,end,meta_data = get_pages_data(request.query_params.get('page', None), activity_flags)
        data = ActivityFlagSerializer(activity_flags[start : end],many=True,context = {"request":request}).data
        return Response({"data":data,"meta":meta_data,"status":status.HTTP_200_OK},status=status.HTTP_200_OK)

class DeleteMyActivityFlagAPI(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    parser_classes = [MultiPartParser,FormParser]

    @swagger_auto_schema(
        tags=['Activity Flags Management'],
        operation_id="Delete activity flag",
        operation_description="Delete activity flag",
        manual_parameters=[
            openapi.Parameter('activity_flag_id', openapi.IN_QUERY, type=openapi.TYPE_STRING,description="activity flag id"),
        ],
    )
    def delete(self, request, *args, **kwargs):
        response = CustomRequiredFieldsValidator.validate_api_field(self, request, [
            {"field_name": "activity_flag_id", "method": "get", "error_message": "Please enter activity flag id"},
        ])
        activity_flag = get_or_none(ActivityFlag, "Invalid activity flag id", id=request.query_params.get('activity_flag_id'),created_by=request.user)
        activity_flag.delete()
        return Response({"message":"Activity Flag Deleted Successfully!","status": status.HTTP_200_OK}, status = status.HTTP_200_OK)

class AddTripAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        tags=['Trip Management'],
        operation_id="Add Trip",
        operation_description="Create a new trip with mapped activities and outfits.",
        manual_parameters=[
            openapi.Parameter('activity',openapi.IN_FORM,type=openapi.TYPE_STRING,description=("[{'activity_flag_id':'ed3rrfe45','outfit_id':'0dere44'},{'activity_flag_id':'ed3rfe45f45','outfit_id':'0dere44'})]")),
            openapi.Parameter('title', openapi.IN_FORM, type=openapi.TYPE_STRING, description="Trip title"),
            openapi.Parameter('description', openapi.IN_FORM, type=openapi.TYPE_STRING, description="Trip description"),
            openapi.Parameter('location', openapi.IN_FORM, type=openapi.TYPE_STRING, description="Trip location"),
            openapi.Parameter('latitude', openapi.IN_FORM, type=openapi.TYPE_STRING, description="Latitude"),
            openapi.Parameter('longitude', openapi.IN_FORM, type=openapi.TYPE_STRING, description="Longitude"),
            openapi.Parameter('start_date', openapi.IN_FORM, type=openapi.TYPE_STRING, description="YYYY-MM-DD"),
            openapi.Parameter('end_date', openapi.IN_FORM, type=openapi.TYPE_STRING ,description="YYYY-MM-DD"),
            # openapi.Parameter('trip_length', openapi.IN_FORM, type=openapi.TYPE_INTEGER, description="Duration in days"),
        ],
    )
    def post(self, request, *args, **kwargs):
        activity_data = request.data.get("activity")
        if not activity_data:
            return Response({"message": "No activity data provided.","status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        
        activity_ids = []
        outfit_ids = []
        if isinstance(activity_data, str):
            try:
                activities = json.loads(activity_data)
            except json.JSONDecodeError:
                return Response(request,{"message": "Invalid JSON format in 'sessions'.","status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        else:
            activities = activity_data

        if Trips.objects.filter(title=request.data.get('title').strip(),created_by=request.user).exists():
            return Response({"message": "Trip already exist for same title !","status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        
        if Trips.objects.filter(start_date=request.data.get('start_date'),end_date=request.data.get('end_date'),created_by=request.user).exists():
            return Response({"message": "Trip already exist for same date !","status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        
        if request.data.get('start_date'):
            try:
                start_date = datetime.strptime(request.data.get('start_date').strip(), "%Y-%m-%d").date()
            except:
                return Response({"message": "Invalid date format. Use YYYY-MM-DD.", "status": status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
            if start_date < date.today():
                return Response({"message": "Start date cannot be in the past.", "status": status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)

        if request.data.get('end_date'):
            try:
                end_date = datetime.strptime(request.data.get('end_date').strip(), "%Y-%m-%d").date()
            except:
                return Response({"message": "Invalid date format. Use YYYY-MM-DD.", "status": status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)

            if end_date < date.today():
                return Response({"message": "End date cannot be in the past.", "status": status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)

        trip = Trips.objects.create(
            title=request.data.get('title').strip(),
            description=request.data.get('description').strip(),
            location=request.data.get('location').strip(),
            latitude=request.data.get('latitude'),
            longitude=request.data.get('longitude'),
            start_date=request.data.get('start_date'),
            end_date=request.data.get('end_date'),
            created_by=request.user
        )
        start = datetime.strptime(trip.start_date, "%Y-%m-%d")
        end = datetime.strptime(trip.end_date, "%Y-%m-%d")
        duration = end - start 
        trip.trip_length = duration.days + 1
        trip.save()
        
        for activity_value in activities:
            activity_id = activity_value['activity_flag_id']
            outfit_id = activity_value['outfit_id']
        
            if activity_id:
                activity_obj = ActivityFlag.objects.filter(id=activity_id).first()
                if activity_obj:
                    activity_ids.append(activity_obj.id)
            if outfit_id:
                outfit_obj = Outfit.objects.filter(id=outfit_id).first()
                if outfit_obj:
                    outfit_ids.append(outfit_obj.id)
        if activity_ids:
            trip.activity_flag.add(*activity_ids)
        if outfit_ids:
            trip.outfit.add(*outfit_ids)
        return Response({"message": "Trip created successfully!","status":status.HTTP_201_CREATED},status=status.HTTP_201_CREATED)
    


class EditTripDetailAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        tags=['Trip Management'],
        operation_id="Edit Trip Details",
        operation_description="Edit trip detail with mapped activities and outfits.",
        manual_parameters=[
            openapi.Parameter('trip_id', openapi.IN_FORM, type=openapi.TYPE_STRING, description="Trip id"),
            openapi.Parameter('activity',openapi.IN_FORM,type=openapi.TYPE_STRING,description=("[{'activity_flag_id':'ed3rrfe45','outfit_id':'0dere44'},{'activity_flag_id':'ed3rfe45f45','outfit_id':'0dere44'})]")),
            openapi.Parameter('title', openapi.IN_FORM, type=openapi.TYPE_STRING, description="Trip title"),
            openapi.Parameter('description', openapi.IN_FORM, type=openapi.TYPE_STRING, description="Trip description"),
            openapi.Parameter('location', openapi.IN_FORM, type=openapi.TYPE_STRING, description="Trip location"),
            openapi.Parameter('latitude', openapi.IN_FORM, type=openapi.TYPE_STRING, description="Latitude"),
            openapi.Parameter('longitude', openapi.IN_FORM, type=openapi.TYPE_STRING, description="Longitude"),
            openapi.Parameter('start_date', openapi.IN_FORM, type=openapi.TYPE_STRING, description="YYYY-MM-DD"),
            openapi.Parameter('end_date', openapi.IN_FORM, type=openapi.TYPE_STRING ,description="YYYY-MM-DD"),
            # openapi.Parameter('trip_length', openapi.IN_FORM, type=openapi.TYPE_INTEGER, description="Duration in days"),
        ],
    )
    def post(self, request, *args, **kwargs):
        trip = get_or_none(Trips,'Trip does not exist !',id = request.data.get('trip_id').strip(),created_by=request.user)
        if request.data.get('title'):
            if Trips.objects.filter(title=request.data.get('title').strip(),created_by=request.user).exists():
                return Response({"message": "Trip already exist for same title !","status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        
        if request.data.get('start_date'):
            if Trips.objects.filter(start_date=request.data.get('start_date'),created_by=request.user).exists():
                return Response({"message": "Trip already exist for same date !","status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        
        if request.data.get('start_date'):
            try:
                start_date = datetime.strptime(request.data.get('start_date').strip(), "%Y-%m-%d").date()
            except:
                return Response({"message": "Invalid date format. Use YYYY-MM-DD.", "status": status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
            if start_date < date.today():
                return Response({"message": "Start date cannot be in the past.", "status": status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)

        if request.data.get('end_date'):
            try:
                end_date = datetime.strptime(request.data.get('end_date').strip(), "%Y-%m-%d").date()
            except:
                return Response({"message": "Invalid date format. Use YYYY-MM-DD.", "status": status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)

            if end_date < date.today():
                return Response({"message": "End date cannot be in the past.", "status": status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)

        if request.data.get('title'):
            trip.title = request.data.get('title').strip()

        if request.data.get('description'):
            trip.description = request.data.get('description').strip()

        if request.data.get('location'):
            trip.location = request.data.get('location').strip()

        if request.data.get('latitude'):
            trip.latitude = request.data.get('latitude').strip()

        if request.data.get('longitude'):
            trip.longitude = request.data.get('longitude').strip()

        if request.data.get('start_date'):
            trip.start_date = request.data.get('start_date').strip()

        if request.data.get('end_date'):
            trip.end_date = request.data.get('end_date').strip()

        try:
            if request.data.get('start_date'):
                start = datetime.strptime(trip.start_date, "%Y-%m-%d")
            if request.data.get('end_date'):
                end = datetime.strptime(trip.end_date, "%Y-%m-%d")
            duration = end - start 
            trip.trip_length = duration.days + 1
        except:
            pass

        trip.save()

        activity_ids = []
        outfit_ids = []
        if request.data.get("activity"):
        
            activity_data = request.data.get("activity")
            if isinstance(activity_data, str):
                try:
                    activities = json.loads(activity_data)
                except json.JSONDecodeError:
                    return Response(request,{"message": "Invalid JSON format in 'sessions'.","status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
            else:
                activities = activity_data
                
            for activity_value in activities:
                activity_id = activity_value['activity_flag_id']
                outfit_id = activity_value['outfit_id']
            
                if activity_id:
                    activity_obj = ActivityFlag.objects.filter(id=activity_id).first()
                    if activity_obj:
                        activity_ids.append(activity_obj.id)
                if outfit_id:
                    outfit_obj = Outfit.objects.filter(id=outfit_id).first()
                    if outfit_obj:
                        outfit_ids.append(outfit_obj.id)
            if activity_ids:
                trip.activity_flag.add(*activity_ids)
            if outfit_ids:
                trip.outfit.add(*outfit_ids)
        return Response({"message": "Trip updated successfully!","status":status.HTTP_201_CREATED},status=status.HTTP_201_CREATED)


class MarkItemFavouriteAPI(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    parser_classes = [MultiPartParser,FormParser]

    @swagger_auto_schema(
        tags=['WarDrobe management'],
        operation_id="Mark Item as favourite",
        operation_description="Mark Item as favourite",
        manual_parameters=[
            openapi.Parameter('item_id', openapi.IN_FORM, type=openapi.TYPE_STRING,description="item id"),
            openapi.Parameter('is_favourite', openapi.IN_FORM, type=openapi.TYPE_STRING,description="1: Favourite , 2 : Not favourite"),
            ],
    )
    def post(self, request, *args, **kwargs):
        response = CustomRequiredFieldsValidator.validate_api_field(self, request, [
            {"field_name": "item_id", "method": "post", "error_message": "Please enter item id"},
            {"field_name": "is_favourite", "method": "post", "error_message": "Please enter any one choices"},
        ])
        item = get_or_none(ClothingItem,"Item id does not exist !" , id = request.data.get('item_id'))
        if item in request.user.favourite_item.all():
            item.favourite.remove(request.user)
            message = "Item unmarked successfully !"
        else:
            item.favourite.add(request.user)
            message = "Item marked as favourite !"
        item.save()
        return Response({"message":message,"status": status.HTTP_200_OK}, status = status.HTTP_200_OK)

class FavouriteItemListAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["WarDrobe management"],
        operation_description="Favourite Item List API",
        operation_id="Favourite Item List API",
        manual_parameters=[
            openapi.Parameter('category_id', openapi.IN_QUERY, type=openapi.TYPE_STRING,description="Category id"),
        ],
    )
    def get(self, request, *args, **kwargs):
        favourite_items = request.user.favourite_item.all()
        if request.query_params.get('category_id'):
            category = get_or_none(ClothCategory,'Category does not exist !',id = request.query_params.get('category_id').strip() )
            favourite_items = favourite_items.filter(cloth_category=category)
        data = ClothItemSerializer(favourite_items,many=True,context = {"request":request}).data
        return Response({"data":data,"status":status.HTTP_200_OK},status=status.HTTP_200_OK)    

class MarkOutfitFavouriteAPI(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    parser_classes = [MultiPartParser,FormParser]

    @swagger_auto_schema(
        tags=['Outfit Management'],
        operation_id="Mark Outfit as favourite",
        operation_description="Mark Outfit as favourite",
        manual_parameters=[
            openapi.Parameter('outfit_id', openapi.IN_FORM, type=openapi.TYPE_STRING,description="outfit id"),
            openapi.Parameter('is_favourite', openapi.IN_FORM, type=openapi.TYPE_STRING,description="1: Favourite , 2 : Not favourite"),
            ],
    )
    def post(self, request, *args, **kwargs):
        response = CustomRequiredFieldsValidator.validate_api_field(self, request, [
            {"field_name": "outfit_id", "method": "post", "error_message": "Please enter item id"},
            {"field_name": "is_favourite", "method": "post", "error_message": "Please enter any one choices"},
        ])
        outfit = get_or_none(Outfit,"Outfit id does not exist !" , id = request.data.get('outfit_id'))
        if outfit in request.user.favourite_outfit.all():
            outfit.favourite.remove(request.user)
            message = "Item unmarked successfully !"
        else:
            outfit.favourite.add(request.user)
            message = "Item marked as favourite !"
        outfit.save()
        return Response({"message":message,"status": status.HTTP_200_OK}, status = status.HTTP_200_OK)


class FavouriteOutfitListAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["Outfit Management"],
        operation_description="Favourite Outfit List API",
        operation_id="Favourite Outfit List API",
        manual_parameters=[],
    )
    def get(self, request, *args, **kwargs):
        favourite_outfits = request.user.favourite_outfit.all()
        data = MyOutFitSerializer(favourite_outfits,many=True,context = {"request":request}).data
        return Response({"data":data,"status":status.HTTP_200_OK},status=status.HTTP_200_OK)   
    
class GetItemByCategoryAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["WarDrobe management"],
        operation_id="Get Item By category",
        operation_description="Get Item By category",
        manual_parameters=[
            openapi.Parameter('category_id', openapi.IN_QUERY, type=openapi.TYPE_STRING,description="Category id"),
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
        ],
    )
    def get(self, request, *args, **kwargs):
        category = get_or_none(ClothCategory,'category does not exist !', id = request.query_params.get('category_id'))
        items = ClothingItem.objects.filter(cloth_category = category,wardrobe__user  = request.user).order_by('created_on')
        start,end,meta_data = get_pages_data(request.query_params.get('page', None), items)
        data = ClothItemSerializer(items[start : end],many=True,context = {"request":request}).data
        return Response({"data":data,"meta":meta_data,"status":status.HTTP_200_OK},status=status.HTTP_200_OK)

class ItemSeachFilterAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["WarDrobe management"],
        operation_id="Search Items",
        operation_description="Search Items",
        manual_parameters=[
            openapi.Parameter('search', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('category_ids', openapi.IN_QUERY, type=openapi.TYPE_ARRAY,items=openapi.Items(type=openapi.TYPE_STRING),description='List of category ids'),
            openapi.Parameter('occasion_id', openapi.IN_QUERY, type=openapi.TYPE_STRING,description='Occasion id'),
            openapi.Parameter('weather_type', openapi.IN_QUERY, type=openapi.TYPE_INTEGER,description='Weather Type'),
            openapi.Parameter('color', openapi.IN_QUERY, type=openapi.TYPE_STRING,description='Colour'),
            openapi.Parameter('sort_by', openapi.IN_QUERY, type=openapi.TYPE_STRING,description="date|alpha|category"),
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
        ],
    )
    def get(self, request, *args, **kwargs):
        wardrobe = get_or_none(Wardrobe,"wardrobe does not exist !",user=request.user)
        items = ClothingItem.objects.filter(wardrobe=wardrobe).order_by("-created_on")
        if request.query_params.get('search'):
            items = items.filter(Q(brand__icontains = request.query_params.get('search'))|
                        Q(color__icontains=request.query_params.get('search'))|
                        Q(title__icontains=request.query_params.get('search'))|
                        Q(cloth_category__title__icontains = request.query_params.get('search'))|
                        Q(occasion__title__icontains = request.query_params.get('search'))|
                        Q(accessory__title__icontains = request.query_params.get('search')))
            
            recent_search = RecentSearch.objects.create(
                user=request.user,
                keyword=request.query_params.get('search'),
            )
        if request.query_params.getlist('category_ids'):
            category_ids = request.query_params.getlist("category_ids")
            if len(category_ids) == 1 and "," in category_ids[0]:
                category_ids = category_ids[0].split(",")

            category_ids = [c.strip() for c in category_ids]
            if category_ids:
                categories = ClothCategory.objects.filter(id__in=category_ids)
                if not categories.exists():
                    return Response({"message": "Category not found!", "status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
                items = items.filter(cloth_category__in=categories)

        if request.query_params.get('occasion_id'):
            occasion  = Occasion.objects.get(id = request.query_params.get('occasion_id'))
            if not occasion:
                return Response({"message":"Occasion not found !","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
            items = items.filter(occasion = occasion)

        if request.query_params.get('weather_type'):
            if not int(request.query_params.get('weather_type')) in [1,2,3,4,5]:
                return Response({"message":"Weather type does not matched!", "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
            items = items.filter(weather_type = int(request.query_params.get('weather_type')))
            
        if request.query_params.get('color'):
            items = items.filter(color__iexact=request.query_params.get('color'))

        sort_by = request.query_params.get('sort_by')
        if sort_by == "date":
            items = items.order_by("-created_on")

        elif sort_by == "alpha":
            items = items.order_by("title")

        elif sort_by == "category":
            items = items.order_by("cloth_category__title")

        else:
            items = items.order_by("-created_on") 

        if not items:
            return Response({"data":[],"status":status.HTTP_200_OK},status=status.HTTP_200_OK)
        start,end,meta_data = get_pages_data(request.query_params.get('page', None), items)
        data = ClothItemSerializer(items[start : end],many=True,context = {"request":request}).data
        return Response({"data":data,"meta":meta_data,"status":status.HTTP_200_OK},status=status.HTTP_200_OK)

class RecentSearchAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["WarDrobe management"],
        operation_description="Get recent searches of user",
        operation_id="Get recent searches of user",
        manual_parameters=[],
    )
    def get(self, request, *args, **kwargs):
        searches = RecentSearch.objects.filter(user=request.user).order_by('-created_on')[:5]
        data = RecentSearchSerializer(searches,many=True,context = {"request":request}).data
        return Response({"data":data,"status":status.HTTP_200_OK},status=status.HTTP_200_OK)

class RemoveItemFromRecentSearchAPI(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    parser_classes = [MultiPartParser,FormParser]

    @swagger_auto_schema(
        tags=['WarDrobe management'],
        operation_id="Delete Items From Recent Search",
        operation_description="Delete Items From Recent Search",
        manual_parameters=[
            openapi.Parameter('search_id', openapi.IN_QUERY, type=openapi.TYPE_STRING)
        ],
    )
    def delete(self, request, *args, **kwargs):
        response = CustomRequiredFieldsValidator.validate_api_field(self, request, [
            {"field_name": "search_id", "method": "get", "error_message": "Please enter search id"},
        ])
        recent_search = get_or_none(RecentSearch, "Invalid search id", id=request.query_params.get('search_id'),user=request.user)
        recent_search.delete()
        return Response({"message":"Recent Search Deleted Successfully!","status": status.HTTP_200_OK}, status = status.HTTP_200_OK)

class RemoveAllItemFromRecentSearchAPI(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    parser_classes = [MultiPartParser,FormParser]

    @swagger_auto_schema(
        tags=['WarDrobe management'],
        operation_id="Delete All Items From  Recent Search",
        operation_description="Delete All Items From Recent Search",
        manual_parameters=[],
    )
    def delete(self, request, *args, **kwargs):
        recent_search = RecentSearch.objects.filter(user=request.user)
        recent_search.delete()
        return Response({"message":"Recent Search Deleted Successfully!","status": status.HTTP_200_OK}, status = status.HTTP_200_OK)


###---------------WearLog management----------------------######

class WearLogAPI(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    parser_classes = [MultiPartParser,FormParser]

    @swagger_auto_schema(
        tags=["Wear Calendar"],
        operation_id="Item wear log",
        operation_description="Item wear log",
        manual_parameters=[
            openapi.Parameter('item_id', openapi.IN_FORM, type=openapi.TYPE_STRING,description="Item Id"),
            openapi.Parameter('date', openapi.IN_FORM, type=openapi.TYPE_STRING,description="YYYY-MM-DD"),
            openapi.Parameter('notes', openapi.IN_FORM, type=openapi.TYPE_STRING,description="Notes"),
        ],
    )
    def post(self, request):
        response = CustomRequiredFieldsValidator.validate_api_field(self, request, [
            {"field_name": "item_id", "method": "post", "error_message": "Please enter Item Id"},
        ])
        item = get_or_none(ClothingItem,"Item not found",id=request.data.get("item_id"),wardrobe__user=request.user)
        if request.data.get("date"):
            try:
                worn_date = datetime.strptime(request.data.get("date").strip(), "%Y-%m-%d").date()
            except:
                return Response({"message": "Invalid date format. Use YYYY-MM-DD.", "status": status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
            if worn_date < date.today():
                return Response({"message": "Wear date cannot be in the past.", "status": status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            worn_date = datetime.strptime(request.data.get("date").strip(), "%Y-%m-%d").date()
        except:
            return Response({"message": "Invalid date format (YYYY-MM-DD)", "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

        wear_entry, created = WearHistory.objects.get_or_create(
            user=request.user,
            item=item,
            worn_on=worn_date,
            defaults={"notes": request.data.get("notes")}
        )
        if not created:
            return Response({"message": "Already marked as worn on this date", "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        item.wear_count += 1 
        item.save()
        return Response({"message": "Wear entry added successfully !","status":status.HTTP_200_OK},status=status.HTTP_200_OK)

class WearCalendarAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        tags=["Wear Calendar"],
        operation_id="Get Item wear logs",
        operation_description="Get Item wear logs",
        manual_parameters=[
            openapi.Parameter('wear_log',openapi.IN_QUERY,type=openapi.TYPE_STRING,description="date or month or year (date='YYYY-MM-DD', month='YYYY-MM', year='YYYY')",),
            openapi.Parameter('date', openapi.IN_QUERY, type=openapi.TYPE_STRING,description='YYYY-MM-DD'),
            openapi.Parameter('year', openapi.IN_QUERY, type=openapi.TYPE_STRING,description='YYYY'),
            openapi.Parameter('month', openapi.IN_QUERY, type=openapi.TYPE_STRING,description='YYYY-MM'),
        ]
    )
    def get(self, request, *args, **kwargs):
        entries = WearHistory.objects.filter(user=request.user)
        wear_log = request.query_params.get("wear_log")
        if wear_log:
            if wear_log == "year":
                year = request.query_params.get("year")
                try:
                    year = int(year)
                    start = date(year, 1, 1)
                    end = date(year + 1, 1, 1)
                except:
                    return Response({"message": "Invalid year format", "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
                entries = WearHistory.objects.filter(user=request.user,worn_on__gte=start,worn_on__lt=end)
                
            elif wear_log == "month":
                month = request.query_params.get("month")
                try:
                    year, month_num = map(int, month.split("-"))
                    start = date(year, month_num, 1)
                    end_month = month_num + 1 if month_num < 12 else 1
                    end_year = year if month_num < 12 else year + 1
                    end = date(end_year, end_month, 1)
                except:
                    return Response({"message": "Invalid month format", "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
                entries = WearHistory.objects.filter(user=request.user,worn_on__gte=start,worn_on__lt=end)
                
            elif wear_log == "date":
                wear_date = request.query_params.get("date")
                try:
                    target_date = datetime.strptime(wear_date, "%Y-%m-%d").date()
                except:
                    return Response({"message": "Invalid date format", "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

                entries = WearHistory.objects.filter(user=request.user,worn_on=target_date)
            else:
                return Response({"message": "Invalid wear_log. Use date/month/year", "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

        start, end, meta_data = get_pages_data(request.query_params.get('page', None), entries)
        data = WearHistorySerializer(entries, many=True, context={"request": request}).data
        return Response({"data": data,  "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)

class GetWearLogsByItemAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["Wear Calendar"],
        operation_id="Get item wear log history",
        operation_description="Get item wear log history",
        manual_parameters=[
            openapi.Parameter('item_id', openapi.IN_QUERY, type=openapi.TYPE_STRING,description="Item id"),
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
        ],
    )
    def get(self, request, *args, **kwargs):
        item_id = get_or_none(ClothingItem,'Item does not exist !', id = request.query_params.get('item_id'))
        wear_logs = WearHistory.objects.filter(item = item_id,user  = request.user).order_by('created_on')
        start,end,meta_data = get_pages_data(request.query_params.get('page', None), wear_logs)
        data = WearHistorySerializer(wear_logs[start : end],many=True,context = {"request":request}).data
        return Response({"data":data,"meta":meta_data,"status":status.HTTP_200_OK},status=status.HTTP_200_OK)

class MostWearClothAnalyticsAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["Wardrobe Analytics"],
        operation_id="Item Usage Frequency",
        operation_description="Analyze usage frequency of wardrobe items.",
        manual_parameters=[
            openapi.Parameter('category_id', openapi.IN_QUERY, type=openapi.TYPE_STRING,description="Category id"),
        ],
       
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        items = ClothingItem.objects.filter(wardrobe__user=user)
        if not items.exists():
            return Response({"message": "No wardrobe items found.","most_worn": [],"least_worn": [],"recommendations": []})

        most_worn = items.order_by('-wear_count')[:5]
        least_worn = items.order_by('wear_count').first()
        most_worn_count = items.order_by('-wear_count').first()
        if request.query_params.get('category_id'):
            category = ClothCategory.objects.get(id = request.query_params.get('category_id'))
            if not category:
                return Response({"message": "Invalid category id","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
            items = items.filter(cloth_category = category)
            most_worn = items.order_by('-wear_count')[:5]

        under_used = items.filter(wear_count__lte=2)
        recommendations = []

        if under_used.exists():
            recommendations.append("Consider wearing your less-used items more often to balance wardrobe usage.")

        over_used_items = items.filter(wear_count__gte=10)
        if over_used_items.exists():
            recommendations.append("Some items are heavily used. Consider refreshing or replacing them.")

        if not recommendations:
            recommendations.append("Your wardrobe usage is well-balanced.")

        wardrobe = get_or_none(Wardrobe, "Wardrobe does not exist!", user=request.user)
        total_items = ClothingItem.objects.filter(wardrobe=wardrobe).count()
        worn_item_ids = (WearHistory.objects.filter(item__wardrobe=wardrobe).values_list('item', flat=True).distinct())

        used_items_count = worn_item_ids.count()
        utilization = (used_items_count / total_items * 100) if total_items else 0

        response = {"stats": {"total_items": ClothingItem.objects.filter(wardrobe__user=user).count(),
                              "least_worn_count": least_worn.wear_count,
                              "most_worn_count": most_worn_count.wear_count,
                              "utilization": utilization,
                              "most_used_item": most_worn[0].title if most_worn else None,
                              "favourite_items":request.user.favourite_item.all().count()},
            "most_worn": ItemUsageFrequencySerializer(most_worn, many=True,context = {"request":request}).data,
            "least_worn": ItemUsageFrequencySerializer(least_worn,context = {"request":request}).data,
            "under_used_items": ItemUsageFrequencySerializer(under_used, many=True,context = {"request":request}).data,
            "recommendations": recommendations,
            
        }

        return Response(response, status=200)


class OutfitRecommendationAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["Trip Management"],
        operation_id="Item Recommened for trip",
        operation_description="Item Recommened for trip",
        manual_parameters=[openapi.Parameter('activity_id', openapi.IN_QUERY,type=openapi.TYPE_STRING,description="Activity ID"),
        ],
    )
    def get(self, request, *args, **kwargs):
        CustomRequiredFieldsValidator.validate_api_field(self, request, 
                [{"field_name": "activity_id","method": "get","error_message": "Please enter activity id"},])
        required_items = []
        user_activity = get_or_none(ActivityFlag,"Activity flag does not exist!",id=request.query_params.get("activity_id").strip())
        key = user_activity.name.lower().replace(" ", "_")
        required_items += ACTIVITY_ITEM_MAP.get(key, [])
        required_items = list(set(required_items))
        cloth_items = ClothingItem.objects.filter(wardrobe__user=request.user,cloth_category__title__in=required_items).select_related("cloth_category")
        
        # missing_items = [
        #     item for item in required_items
        #     if item not in owned_categories
        # ]
      
        # store_items = StoreItem.objects.filter(category__in=missing_items)
        # for item in store_items:
        #     Recommendation.objects.create(
        #         vacation_plan=user_trip,
        #         recommended_item=item.title,
        #         category=item.category,
        #         purchase_link=item.link,
        #         reason="You don't have this item; recommended for your trip"
        #     )

        data = ClothItemSerializer(cloth_items,many=True,context = {"request":request}).data
        return Response({"data":data,"status":status.HTTP_200_OK},status=status.HTTP_200_OK)



class ShareWardrobeAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["WarDrobe management"],
        operation_id="share digitized wardrobes with friends or family members",
        operation_description="share digitized wardrobes with friends or family members",
        manual_parameters=[
            openapi.Parameter('user_email', openapi.IN_FORM,type=openapi.TYPE_STRING,description="User Email"),
        ],
    )
    def post(self, request, *args, **kwargs):
        CustomRequiredFieldsValidator.validate_api_field(self, request, 
                [{"field_name": "user_email","method": "post","error_message": "Please enter user email"},])
        
        user_email = request.data.get("user_email")
        share_friend = get_or_none(User,'User does not exist !',email=user_email)
        wardrobe = Wardrobe.objects.filter(user=request.user).first()
        if not wardrobe:
            return Response({"message": "No wardrobe found for current user.", "status": status.HTTP_400_BAD_REQUEST},status=status.HTTP_404_NOT_FOUND)

        if share_friend in wardrobe.shared_with.all():
            return Response({"message": "This wardrobe is already shared with this user.", "status": status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        
        wardrobe.shared_with.add(share_friend)
        wardrobe_path = reverse("frontend:view_shared_wardrobe")
        wardrobe_link = f"{request.build_absolute_uri(wardrobe_path)}?wardrobe_id={wardrobe.id}"
        wardrobe.is_shared = True
        wardrobe.share_count = wardrobe.share_count + 1
        wardrobe.save()

        send_notification(
            created_by=get_admin(),
            created_for=[share_friend],
            title=f"Wardrobe share",
            description=f"share digitized wardrobes with {share_friend.email}",
            notification_type=ADMIN_NOTIFICATION,
            obj_id=str(share_friend.id),
        )
        bulk_send_user_email(request,request.user,'EmailTemplates/ShareWardrobe.html','A Wardrobe Has Been Shared With You!',share_friend.email,wardrobe_link,"","","","",assign_to_celery=False)
        return Response({"wardrobe_link":wardrobe_link,"status":status.HTTP_200_OK},status=status.HTTP_200_OK)
    

class GetWardrobeDetailsAPI(APIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["WarDrobe management"],
        operation_id="View wardrobe details",
        operation_description="Retrieve wardrobe details or outfits based on type",
        manual_parameters=[
            openapi.Parameter('wardrobe_id', openapi.IN_QUERY, type=openapi.TYPE_STRING, description="Wardrobe ID",required=True),
            openapi.Parameter('type', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description="1 = Items, 2 = Outfits",required=True),
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        ],
    )
    def get(self, request,*arge,**kwargs):
        wardrobe_id = request.query_params.get("wardrobe_id")
        req_type = request.query_params.get("type")
        if not wardrobe_id:
            return Response({"error": "wardrobe_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not req_type:
            return Response({"error": "type is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            req_type = int(req_type)
        except ValueError:
            return Response({"error": "type must be 1 or 2"}, status=status.HTTP_400_BAD_REQUEST)

        wardrobe = Wardrobe.objects.filter(id=wardrobe_id).first()
        if not wardrobe:
            return Response({"error": "Invalid wardrobe_id"}, status=status.HTTP_404_NOT_FOUND)
        if req_type == 1:
            data = WardrobeSerializer(wardrobe,context={"request": request}).data

            return Response({"data": data},status=status.HTTP_200_OK)
        if req_type == 2:
            user_outfits = Outfit.objects.filter(created_by=wardrobe.user).order_by("-created_on")
            start, end, meta_data = get_pages_data(request.query_params.get("page"),user_outfits)
            data = MyOutFitSerializer(user_outfits[start:end],many=True,context={"request": request}).data
            return Response({"data": data,"meta": meta_data},status=status.HTTP_200_OK)

        return Response({"error": "Invalid type. Allowed values: 1 = Items, 2 = Outfits"},status=status.HTTP_400_BAD_REQUEST)
