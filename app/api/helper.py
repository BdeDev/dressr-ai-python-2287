import random
import logging
from accounts.models import *
from rest_framework.exceptions import ValidationError
from rest_framework import status
db_logger = logging.getLogger('db')


class RequiredFieldValidations():
    '''
        Validates empty fields for APIs
    '''
    def validate_field(self,request,field_name,method,error_message):
        if method.lower() == "post":
            if not request.data.get(f'{field_name}'):
                raise ValidationError({"message": error_message, "status": status.HTTP_400_BAD_REQUEST})
        elif method.lower() == "file":
            if not request.FILES.get(f'{field_name}'):
                raise ValidationError({"message": error_message, "status": status.HTTP_400_BAD_REQUEST})
        else:
            if not request.query_params.get(f'{field_name}'):
                raise ValidationError({"message": error_message, "status": status.HTTP_400_BAD_REQUEST}) 
