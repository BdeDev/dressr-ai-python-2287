
from rest_framework.exceptions import ValidationError
from rest_framework import status
from django.db.models import Q
from accounts.models import User
from django.contrib import messages
from accounts.constants import *


class CustomRequiredFieldsValidator:
    """
    Custom validator to check required fields in API requests.
    """

    def validate_api_field(self, request, fields_list=None):
        if fields_list is None:
            fields_list = []

        return_data = {}

        for field_data in fields_list:
            field_name = field_data.get("field_name")
            method = field_data.get("method", "").lower()
            error_message = field_data.get("error_message", "This field is required.")
            choice_options = field_data.get("choice_options")
            return_field = field_data.get("return_field", False)

            # Select source based on method
            if method == "post":
                value = request.data.get(field_name)
            elif method == "file":
                value = request.FILES.get(field_name)
            else:  # Default to GET/query_params
                value = request.query_params.get(field_name)

            # Validate presence
            if value in [None, "", []]:
                raise ValidationError({"message": error_message, "status": status.HTTP_400_BAD_REQUEST})

            # Validate choice options if provided
            if choice_options and value not in choice_options:
                raise ValidationError({"message": error_message, "status": status.HTTP_400_BAD_REQUEST})

            # Collect value if needed
            if return_field:
                return_data[field_name] = value

        return return_data
                               

    def validate_web_field(self, request, fields_list=None):
        """
        Validate required fields for web requests.
        Returns a dict of field values if valid, otherwise returns False and adds error messages.

        fields_list example:
        [
            {"field_name": "field_name", "method": "get", "error_message": ""},
            {"field_name": "field_name", "method": "post", "error_message": ""},
            {"field_name": "field_name", "method": "file", "error_message": ""},
            {"field_name": "field_name", "method": "post", "error_message": "", "choice_options": ['1','2','3']},
        ]
        """
        if fields_list is None:
            fields_list = []

        return_data = {}
        email_restrictions = {"gmail.com", "toxsl.com", "ozvid.com"}

        for field_data in fields_list:
            field_name = field_data.get("field_name")
            method = field_data.get("method", "").lower()
            error_message = field_data.get("error_message", "This field is required.")
            choice_options = field_data.get("choice_options")

            # Get the value based on method
            if method == "post":
                value = request.POST.get(field_name)
            elif method == "file":
                value = request.FILES.get(field_name)
            else:  # default to GET
                value = request.GET.get(field_name)

            # Validate presence
            if not value:
                messages.error(request, error_message)
                return False

            # Validate choice options if provided
            if choice_options and value not in choice_options:
                messages.error(request, error_message)
                return False

            # Restrict certain email domains if field is 'email' and method is 'post'
            if method == "post" and field_name == "email":
                try:
                    domain = value.split("@")[1].lower()
                except IndexError:
                    messages.error(request, "Invalid email format.")
                    return False
                if domain in email_restrictions:
                    messages.error(
                        request,
                        "Please enter an email not ending with gmail.com, toxsl.com, or ozvid.com."
                    )
                    return False

            return_data[field_name] = value

        return return_data


    def validate_unique_field(self, request, is_api, redirect_url, email, mobile_no, user):
        '''
            Validates unique email and mobile number for User model only
            Args:
                request (HttpRequest) : Request (object)
                is_api (bool) : True or False based on api view or web view
                redirect_url (str) : redirect url to redirct in case of duplicate error on web view
                email (str): email string
                mobile_no (str): mobile number (str)
                user (User): `User` object ( If want to exclude this user , in update user api case )
        '''
        validated_data = {"is_valid":True,"error_message":""}
        if user:
            if email:
                if User.objects.filter(Q(status=ACTIVE)|Q(status=INACTIVE),email=email.strip()).exclude(id=user.id).exists():
                    validated_data['is_valid'] = False
                    validated_data['error_message'] = "This email address is already in use , please choose another"
            elif mobile_no:
                if User.objects.filter(Q(status=ACTIVE)|Q(status=INACTIVE),mobile_no=mobile_no.strip()).exclude(id=user.id).exists():
                    validated_data['is_valid'] = False
                    validated_data['error_message'] = "This mobile number is already in use , please choose another"
        else:
            if email:
                if User.objects.filter(Q(status=ACTIVE)|Q(status=INACTIVE),email=email.strip()).exists():
                    validated_data['is_valid'] = False
                    validated_data['error_message'] = "This email address is already in use , please choose another"
            elif mobile_no:
                if User.objects.filter(Q(status=ACTIVE)|Q(status=INACTIVE),mobile_no=mobile_no.strip()).exists():
                    validated_data['is_valid'] = False
                    validated_data['error_message'] = "This mobile number is already in use , please choose another"

        if is_api and validated_data.get('is_valid') == False:
            ## its on api view and have duplicate error 
            raise ValidationError({"message": validated_data.get('error_message'), "status": status.HTTP_400_BAD_REQUEST})

        elif (not is_api ) and (validated_data.get('is_valid') == False):
            ## its on web view and have duplicate error
            messages.error(request, validated_data.get('error_message'))
            raise
       
        return validated_data
