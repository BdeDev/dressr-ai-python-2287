from accounts.common_imports import *
from .serializer import *
from .healper import *

class GetWardrobs(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["WarDrobe management"],
        operation_id="Get Wardrobs",
        operation_description="Get Wardrobs",
        manual_parameters=[]
    )
    def get(self, request, *args, **kwargs):
        # response = CustomRequiredFieldsValidator.validate_api_field(self, request, [
        #     {"field_name": "wardrobe_id", "method": "get", "error_message": "Please enter wardrobe id"},
        # ])
        wardrobe = Wardrobe.objects.filter(user=request.user)
        if not wardrobe:
            return Response({"data":[],"status":status.HTTP_200_OK},status=status.HTTP_200_OK)
        
        start,end,meta_data = get_pages_data(request.query_params.get('page', None), wardrobe)
        data = WardrobeSerializer(wardrobe[start : end],many=True,context = {"request":request}).data
        return Response({"data":data,"meta":meta_data,"status":status.HTTP_200_OK},status=status.HTTP_200_OK)
    

class GetWardrobe(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["WarDrobe management"],
        operation_id="wardrobe view",
        operation_description="wardrobe view",
        manual_parameters=[
            openapi.Parameter('wardrobe_id', openapi.IN_QUERY, type=openapi.TYPE_STRING,description='Wardrobe Id'),
        ],
    )
    def get(self, request, *args, **kwargs):
        wardrobe = get_or_none(Wardrobe, "Invalid wardrobe id", id=request.query_params.get('wardrobe_id'),user=request.user)
        data = WardrobeSerializer(wardrobe,context = {"request":request}).data
        return Response({"data":data,"status":status.HTTP_200_OK},status=status.HTTP_200_OK)

class AddWardrobe(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["WarDrobe management"],
        operation_id="Add Wardrobe",
        operation_description="Add Wardrobe",
        manual_parameters=[
            openapi.Parameter('name', openapi.IN_FORM, type=openapi.TYPE_STRING,description='Wardrobe Name'),
        ],
    )
    def post(self, request, *args, **kwargs):
        ## Validate Required Fields
        response = CustomRequiredFieldsValidator.validate_api_field(self, request, [
            {"field_name": "name", "method": "post", "error_message": "Please enter wardrobe name"},
        ])
        user = request.user        
        if Wardrobe.objects.filter(user=user,name = request.data.get('name')).exists():
            return Response({"message": "Wardrobe already exist with the same name", "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)
        wardrobe = Wardrobe.objects.create(
            name = request.data.get('name'),
            user = user
        )
        return Response({"message": "Wardrobe created successfully!", "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)
    
class EditWardrobe(APIView):
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
    
class DeleteWardrobe(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    parser_classes = [MultiPartParser,FormParser]

    @swagger_auto_schema(
        tags=['WarDrobe management'],
        operation_id="Delete wardrobe",
        operation_description="Delete wardrobe",
        manual_parameters=[
            openapi.Parameter('wardrobe_id', openapi.IN_QUERY, type=openapi.TYPE_STRING)
        ],
    )
    def delete(self, request, *args, **kwargs):
        response = CustomRequiredFieldsValidator.validate_api_field(self, request, [
            {"field_name": "wardrobe_id", "method": "get", "error_message": "Please enter wardrobe id"},
        ])
        wardrobe = get_or_none(Wardrobe, "Invalid wardrobe id", id=request.query_params.get('wardrobe_id'))
        wardrobe.delete()
        return Response({"message":"Wardrobe Deleted Successfully!","status": status.HTTP_200_OK}, status = status.HTTP_200_OK)

class AddClothItem(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["WarDrobe management"],
        operation_id="Add Cloth Items",
        operation_description="Add Cloth Items",
        manual_parameters=[
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
            {"field_name": "wardrobe_id", "method": "post", "error_message": "Please enter wardrobe id"},
            {"field_name": "category_id", "method": "post", "error_message": "Please enter cloth category id"},
            {"field_name": "occasion_id", "method": "post", "error_message": "Please enter occasion id"},
            {"field_name": "accessory_id", "method": "post", "error_message": "Please enter accessory id"},
            {"field_name": "weather_type", "method": "post", "error_message": "Please enter  weather type "},
            {"field_name": "color", "method": "post", "error_message": "Please enter color"},
            {"field_name": "brand", "method": "post", "error_message": "Please enter brand"},
            {"field_name": "price", "method": "post", "error_message": "Please enter price"},
            {"field_name": "image", "method": "post", "error_message": "Please upload image"},
        ])
        user = request.user 
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
        
        cloth_items = ClothingItem.objects.create(
            wardrobe = wardrobe,
            cloth_category = category,
            occasion = occasion,
            accessory  = accessory,
            weather_type = int(request.data.get('weather_type')),
            color = request.data.get('color'),
            brand = request.data.get('brand'),
            price = request.data.get('price'),
            date_added = datetime.now(),
            image = request.FILES.get('image')
        )
        return Response({"message": "Cloth item addedd successfully!","status":status.HTTP_200_OK},status=status.HTTP_200_OK)

class RemoveClothFromWardrobe(APIView):
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

class GetClothItem(APIView):
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
    
class GetCloths(APIView):
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
        wardrobe = get_or_none(Wardrobe, "Invalid wardrobe id", id=request.query_params.get('wardrobe_id'),user=request.user)
        cloth_item = ClothingItem.objects.filter(wardrobe = wardrobe)
        start,end,meta_data = get_pages_data(request.query_params.get('page', None), cloth_item)
        data = ClothItemSerializer(cloth_item[start : end],many=True,context = {"request":request}).data
        return Response({"data":data,"meta":meta_data,"status":status.HTTP_200_OK},status=status.HTTP_200_OK)
    
class EditWardrobeItem(APIView):
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