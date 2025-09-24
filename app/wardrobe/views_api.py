from accounts.common_imports import *
from .serializer import *
from .healper import *


class UserWardrobe(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["WarDrobe management"],
        operation_id="wardrobe view",
        operation_description="wardrobe view",
        manual_parameters=[],
    )
    def get(self, request, *args, **kwargs):
        try:
            wardrobe=Wardrobe.objects.get(user=request.user)
        except:
            return Response({"message":"Wardrobe doe's not exist!","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        data = WardrobeSerializer(wardrobe,context = {"request":request}).data
        return Response({"data":data,"status":status.HTTP_200_OK},status=status.HTTP_200_OK)
    

class BulkUploadItem(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["WarDrobe management"],
        operation_id="Bulk Upload Items",
        operation_description="Bulk Upload Items",
        manual_parameters=[
            openapi.Parameter('wardrobe_id', openapi.IN_FORM, type=openapi.TYPE_STRING,description='Wardrobe ID'),
            openapi.Parameter('file', openapi.IN_FORM, type=openapi.TYPE_FILE,description='File'),
        ],
    )
    def post(self, request, *args, **kwargs):
        ## Validate Required Fields
        response = CustomRequiredFieldsValidator.validate_api_field(self, request, [
            {"field_name": "wardrobe_id", "method": "post", "error_message": "Please enter wardrobe id"},
            {"field_name": "file", "method": "post", "error_message": "Please upload file"},
        ])

        user = request.user        
        wardrobe = Wardrobe.objects.get(user=user,id=request.data.get('wardrobe_id'))
        if not wardrobe:
            return Response({"message": "Wardrobe does not exist", "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        
        if request.FILES.get('file'):
            bulk_upload_items(request.FILES.get('file'))
        return Response({"message": "Bulk Upload Items created successfully!", "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)