from accounts.common_imports import *
from .serializer import *
from .healper import *

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
            openapi.Parameter('title', openapi.IN_FORM, type=openapi.TYPE_FILE, description='title'),
            openapi.Parameter('category_id', openapi.IN_FORM, type=openapi.TYPE_STRING, description='Cloth category ID (e.g., Shirts, Jeans, Shoes)'),
            openapi.Parameter('occasion_id', openapi.IN_FORM, type=openapi.TYPE_STRING, description='Occasion ID'),
            openapi.Parameter('accessory_id', openapi.IN_FORM, type=openapi.TYPE_STRING, description='Accessory ID (e.g., Watch, Bag, Earrings)'),
            openapi.Parameter('weather_type', openapi.IN_FORM, type=openapi.TYPE_STRING, description='1: Summer, 2: Winter, 3: Rainy, 4: Spring, 5: All Season'),
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
            title = request.data.get('title').strip(),
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
        return Response({"message": "Item added successfully!","status": status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
    
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
        manual_parameters=[
            openapi.Parameter('wardrobe_id', openapi.IN_QUERY, type=openapi.TYPE_STRING)
        ],
    )
    def get(self, request, *args, **kwargs):
        response = CustomRequiredFieldsValidator.validate_api_field(self, request, [
            {"field_name": "wardrobe_id", "method": "get", "error_message": "Please enter wardrobe id"},
        ])
        wardrobe = get_or_none(Wardrobe, "Invalid wardrobe id", id=request.query_params.get('wardrobe_id').strip(),user=request.user)
        cloth_item = ClothingItem.objects.filter(wardrobe = wardrobe)
        start,end,meta_data = get_pages_data(request.query_params.get('page', None), cloth_item)
        data = ClothItemSerializer(cloth_item[start : end],many=True,context = {"request":request}).data
        return Response({"data":data,"meta":meta_data,"status":status.HTTP_200_OK},status=status.HTTP_200_OK)
    
class EditWardrobeItemAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["WarDrobe management"],
        operation_id="Edit Wardrobe",
        operation_description="Edit Wardrobe",
        manual_parameters=[
            openapi.Parameter('cloth_item_id', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('wardrobe_id', openapi.IN_FORM, type=openapi.TYPE_STRING,description='Wardrobe Id'),
            openapi.Parameter('category_id', openapi.IN_FORM, type=openapi.TYPE_STRING,description='Cloth category Id'),
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
            {"field_name": "image", "method": "post", "error_message": "Please enter wardrobe name"},
        ])
        user = request.user 
        cloth_item = get_or_none(ClothingItem, "Invalid cloth item id", id=request.data.get('cloth_item_id'))
        wardrobe = Wardrobe.objects.get(id=request.data.get('wardrobe_id'))
        category = ClothCategory.objects.get(id = request.data.get('category_id'))
        occasion = Occasion.objects.get(id = request.data.get('occasion_id'))
        accessory = Accessory.objects.get(id = request.data.get('accessory_id'))

        if not wardrobe:
            return Response({"message": "Wardrobe does not exist!", "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        if not category:
            return Response({"message": "Category does not exist!", "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        if not occasion:
            return Response({"message": "Occasion does not exist!", "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        if not accessory:
            return Response({"message": "Accessory does not exist!", "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        if not int(request.data.get('weather_type')) in [1,2,3,4,5]:
            return Response({"message":"Weather type does not matched!", "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        
        cloth_item.wardrobe = wardrobe
        cloth_item.cloth_category = category
        cloth_item.accessory = accessory
        cloth_item.occasion = occasion
        cloth_item.weather_type = int(request.data.get('weather_type'))
        cloth_item.color = request.data.get('color')
        cloth_item.brand = request.data.get('brand')
        cloth_item.price = request.data.get('price')
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
        operation_id="Get All ClothCategories",
        operation_description="Get All ClothCategories",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
        ],
    )
    def get(self, request, *args, **kwargs):
        occasions = ClothCategory.objects.all().order_by('-created_on')
        start,end,meta_data = get_pages_data(request.query_params.get('page', None), occasions)
        data = ClothCategorySerializer(occasions[start : end],many=True,context = {"request":request}).data
        return Response({"data":data,"meta":meta_data,"status":status.HTTP_200_OK},status=status.HTTP_200_OK)

class CreateOutfitAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["Outfit Management"],
        operation_id="Create Outfit",
        operation_description="Create Outfit",
        manual_parameters=[
            openapi.Parameter('accessory_ids', openapi.IN_FORM, type=openapi.TYPE_ARRAY,items=openapi.Items(type=openapi.TYPE_STRING), description='List of Accessory IDs'),
            openapi.Parameter('category_ids', openapi.IN_FORM, type=openapi.TYPE_ARRAY,items=openapi.Items(type=openapi.TYPE_STRING), description='List of Category IDs'),
            openapi.Parameter('occasion_id', openapi.IN_FORM, type=openapi.TYPE_STRING, description='Occasion ID'),
            openapi.Parameter('weather_type', openapi.IN_FORM, type=openapi.TYPE_STRING, description='1:Summer, 2:Winter, 3:Rainy, 4:Spring, 5:All Season'),
            openapi.Parameter('color', openapi.IN_FORM, type=openapi.TYPE_STRING, description='Color'),
            openapi.Parameter('title', openapi.IN_FORM, type=openapi.TYPE_STRING, description='Outfit'),
        ],
    )
    def post(self, request):
        user = request.user
       
        if request.data.get('accessory_ids'):
            valid_accessories = Accessory.objects.filter(id__in=request.data.get('accessory_ids').split(','))
           
        if request.data.get('category_ids'):
            valid_categories = ClothCategory.objects.filter(id__in=request.data.get('category_ids').split(','))

        occasion = Occasion.objects.filter(id=request.data.get('occasion_id')).first()
        if not occasion:
            return Response({"message": "Invalid occasion ID.","status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

        if int(request.data.get('weather_type')) not in [1, 2, 3, 4, 5]:
            return Response({"message": "Invalid weather type","status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        # Build the clothing item query
        items = ClothingItem.objects.filter(wardrobe__user=user)

        # Combine filters more cleanly
        items = items.filter(
            Q(weather_type=int(request.data.get('weather_type'))) | Q(occasion_id=occasion),
            Q(cloth_category__in=valid_categories) | Q(accessory__in=valid_accessories)
            )
        
     
        # if request.data.get('color'):
        #     items = items.filter(Q(color__iexact=request.data.get('color')) | Q(color__isnull=True))

        if not items.exists():
            return Response({"message": "No matching clothing items found for the given filters.", "status": status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)

        outfit = Outfit.objects.create(
            title=request.data.get('title').strip() ,
            occasion=occasion,
            weather_type=int(request.data.get('weather_type')),
            created_by=user,
            color=request.data.get('color')
        )
        outfit.items.set(items)
        return Response({"message": "Outfit created successfully!","outfit_id": outfit.id,"total_items": items.count(),"status": status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)

class MyOutFitListAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["Outfit Management"],
        operation_id="Get All My Outfit",
        operation_description="Get All My Outfit",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
        ],
    )
    def get(self, request, *args, **kwargs):
        outfits = Outfit.objects.filter(created_by=request.user).order_by('-created_on')
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
        outfit = get_or_none(Outfit, "Invalid outfit id", id=request.query_params.get('outfit_id'))
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
        ],
    )
    def post(self, request, *args, **kwargs):
        ## Validate Required Fields
        response = CustomRequiredFieldsValidator.validate_api_field(self, request, [
            {"field_name": "outfit_id", "method": "post", "error_message": "Please enter outfit id"},
        ])
        user = request.user 
        outfit = get_or_none(Outfit, "Invalid outfit id", id=request.data.get('outfit_id'),created_by=request.user)

        if request.data.get('accessory_ids'):
            valid_accessories = Accessory.objects.filter(id__in=request.data.get('accessory_ids').split(','))
           
        if request.data.get('category_ids'):
            valid_categories = ClothCategory.objects.filter(id__in=request.data.get('category_ids').split(','))

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
            openapi.Parameter('item_id', openapi.IN_FORM, type=openapi.TYPE_STRING,description="Item id")
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
        outfit.save()
        return Response({"message":"Outfit addedd Successfully!","status": status.HTTP_200_OK}, status = status.HTTP_200_OK)


# class AddTripAPI(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#     parser_classes = [MultiPartParser, FormParser]

#     @swagger_auto_schema(
#         tags=['Trip Management'],
#         operation_id="Add trip",
#         operation_description="Add a new trip for the user",
#         manual_parameters=[
#             openapi.Parameter('activity', openapi.IN_FORM, type=openapi.TYPE_STRING, description="Activity Flag ID"),
#             openapi.Parameter('activity_flag', openapi.IN_FORM, type=openapi.TYPE_STRING, description="{'name':'fgas','description':'dshdhdf'} (if creating a new one)"),
#             openapi.Parameter('title', openapi.IN_FORM, type=openapi.TYPE_STRING, description="Trip title"),
#             openapi.Parameter('description', openapi.IN_FORM, type=openapi.TYPE_STRING, description="Trip description"),
#             openapi.Parameter('location', openapi.IN_FORM, type=openapi.TYPE_STRING, description="Trip location"),
#             openapi.Parameter('latitude', openapi.IN_FORM, type=openapi.TYPE_STRING, description="Latitude"),
#             openapi.Parameter('longitude', openapi.IN_FORM, type=openapi.TYPE_STRING, description="Longitude"),
#             openapi.Parameter('start_date', openapi.IN_FORM, type=openapi.TYPE_STRING, description="YYYY-MM-DD"),
#             openapi.Parameter('end_date', openapi.IN_FORM, type=openapi.TYPE_STRING, description="YYYY-MM-DD"),
#             openapi.Parameter('trip_length', openapi.IN_FORM, type=openapi.TYPE_STRING, description="Duration in days"),
#         ],
#     )
#     def post(self, request, *args, **kwargs):
#         required_fields = ['title', 'description', 'location', 'start_date', 'end_date', 'trip_length']
#         missing = [f for f in required_fields if not request.data.get(f)]
#         if missing:
#             return Response(
#                 {"message": f"Missing required fields: {', '.join(missing)}", "status": status.HTTP_400_BAD_REQUEST},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
        
#         activity_flag_obj = None
#         activity_flag_data = request.data.get('activity_flag')
#         activity_id = request.data.get('activity')
#         if activity_flag_data:
#             activity_flag_json = json.loads(activity_flag_data)
#             activity_flag_obj, _ = ActivityFlag.objects.get_or_create(name=activity_flag_json.get('name').strip(),description=activity_flag_json.get('description').strip())
#         elif activity_id:
#             activity_flag_obj = get_or_none(ActivityFlag, "Invalid activity flag ID", id=activity_id)
#         else:
#             return Response({"message": "Please provide either 'activity' or 'activity_flag'.", "status": status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
#         trip, created = Trips.objects.get_or_create(
#             title=request.data.get('title').strip(),
#             description=request.data.get('description').strip(),
#             location=request.data.get('location').strip(),
#             latitude=request.data.get('latitude'),
#             longitude=request.data.get('longitude'),
#             created_by=request.user,
#             activity_flag=activity_flag_obj,
#             start_date=request.data.get('start_date'),
#             end_date=request.data.get('end_date'),
#             trip_length=int(request.data.get('trip_length'))
#         )
#         message = "Trip created successfully!" if created else "Trip already exists."
#         return Response({"message": message, "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)

class GetMyAllTripAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["Trip Management"],
        operation_id="Get All My Trips",
        operation_description="Get All My Trips",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
        ],
    )
    def get(self, request, *args, **kwargs):
        trips = Trips.objects.filter(created_by=request.user).order_by('-created_on')
        start,end,meta_data = get_pages_data(request.query_params.get('page', None), trips)
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
            {"field_name": "trip", "method": "get", "error_message": "Please enter outfit id"},
        ])
        trip = get_or_none(Trips, "Invalid outfit id", id=request.query_params.get('outfit_id'))
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
            openapi.Parameter('trip_length', openapi.IN_FORM, type=openapi.TYPE_INTEGER, description="Duration in days"),
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

        trip = Trips.objects.create(
            title=request.data.get('title').strip(),
            description=request.data.get('description').strip(),
            location=request.data.get('location').strip(),
            latitude=request.data.get('latitude'),
            longitude=request.data.get('longitude'),
            start_date=request.data.get('start_date'),
            end_date=request.data.get('end_date'),
            trip_length=int(request.data.get('trip_length')),
            created_by=request.user
        )
        
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