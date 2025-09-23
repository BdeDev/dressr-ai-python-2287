import logging
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.contrib import messages

db_logger = logging.getLogger('db')

class CustomRequiredFieldsValidator():
    '''
    Custom class to validate all required fields
    '''
    def validate_api_field(self,request,fields_list=[]):
        '''
        Use this function to validate required fields for api view
        in fields_list data will be in dict like 
        choice_options - will be use for select fields or option field
        [
            {"field_name": "field_name", "method": "get", "error_message": ""},
            {"field_name": "field_name", "method": "post", "error_message": ""},
            {"field_name": "field_name", "method": "file", "error_message": ""},
        ]
        '''
        if fields_list:
            for field_data in fields_list:
                field_name = field_data.get("field_name")
                method = field_data.get("method")
                error_message = field_data.get("error_message")
                if method.lower() == "post":
                    if not request.data.get(f'{field_name}'):
                        raise ValidationError({"message": error_message, "status": status.HTTP_400_BAD_REQUEST})

                elif method.lower() == "file":
                    if not request.FILES.get(f'{field_name}'):
                        raise ValidationError({"message": error_message, "status": status.HTTP_400_BAD_REQUEST})
                else:
                    if not request.query_params.get(f'{field_name}'):
                        raise ValidationError({"message": error_message, "status": status.HTTP_400_BAD_REQUEST}) 
                   
                               
    def validate_web_field(self,request,fields_list=[]):
        '''
        Use this function to validate required fields for Web functions view 
        return false added when required field value is not found  ( Use this and store value in a valiable and return on false value)
        in fields_list data will be in dict like 
        choice_options - will be use for select fields or option field
        [
            {"field_name": "field_name", "method": "get", "error_message": ""},
            {"field_name": "field_name", "method": "post", "error_message": ""},
            {"field_name": "field_name", "method": "file", "error_message": ""},
        ]
        '''
        if fields_list:
            for field_data in fields_list:
                field_name = field_data.get("field_name")
                method = field_data.get("method")
                error_message = field_data.get("error_message")
                if method.lower() == "post":
                    if not request.POST.get(f'{field_name}'):
                        messages.error(request,error_message)
                        return False 
                elif method.lower() == "file":
                    if not request.FILES.get(f'{field_name}'):
                        messages.error(request,error_message)
                        return False 
                    
                else:
                    if not request.GET.get(f'{field_name}'):
                        messages.error(request,error_message)
                        return False 
        return True