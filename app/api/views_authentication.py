from accounts.utils import *
from contact_us.models import *
from static_pages.models import *
from accounts.common_imports import *
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout,login,authenticate
from .serializer import *
from api.helper import *
import re
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

"""
Authentication Management
"""
class UserSignupView(APIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = [MultiPartParser,FormParser]

    @swagger_auto_schema(
        tags=["Authentication API's"],
        operation_id="User Signup",
        operation_description="User Signup",
        manual_parameters=[
            openapi.Parameter('first_name', openapi.IN_FORM, type=openapi.TYPE_STRING ,description='First Name'),
            openapi.Parameter('last_name', openapi.IN_FORM, type=openapi.TYPE_STRING ,description='Last Name'),
            openapi.Parameter('email', openapi.IN_FORM, type=openapi.TYPE_STRING ,description='Email Address'),
            openapi.Parameter('mobile_no', openapi.IN_FORM, type=openapi.TYPE_STRING ,description='Mobile Number'),
            openapi.Parameter('country_code', openapi.IN_FORM, type=openapi.TYPE_STRING ,description='Country Code'),
            openapi.Parameter('country_iso_code', openapi.IN_FORM, type=openapi.TYPE_STRING ,description='Country ISO Code'),
            openapi.Parameter('password', openapi.IN_FORM, type=openapi.TYPE_STRING,description='Password'),
            openapi.Parameter('confirm_password', openapi.IN_FORM, type=openapi.TYPE_STRING,description='Confirm Password'),
            openapi.Parameter('device_type', openapi.IN_FORM, type=openapi.TYPE_NUMBER , description='1 for Android and 2 for IOS'),
            openapi.Parameter('device_name', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('device_token', openapi.IN_FORM, type=openapi.TYPE_STRING),
        ]
    )
    def post(self, request, *args, **kwargs):
        ## validate all required fields 
        response=CustomRequiredFieldsValidator.validate_api_field(self,request,
            [
                {"field_name": "first_name", "method": "post", "error_message": "Please enter first name"},
                {"field_name": "last_name", "method": "post", "error_message": "Please enter last name"},
                {"field_name": "email", "method": "post", "error_message": "Please enter email"},
                {"field_name": "mobile_no", "method": "post", "error_message": "Please enter mobile number"},
                {"field_name": "country_code", "method": "post", "error_message": "Please enter country code"},
                {"field_name": "country_iso_code", "method": "post", "error_message": "Please enter country iso code"},
                {"field_name": "password", "method": "post", "error_message": "Please enter password"},
                {"field_name": "confirm_password", "method": "post", "error_message": "Please enter confirm password"},
                {"field_name": "device_type", "method": "post", "error_message": "Please enter device type"},
                {"field_name": "device_name", "method": "post", "error_message": "Please enter device name"},
                {"field_name": "device_token", "method": "post", "error_message": "Please enter device token"},
               
            ]
        )

        match = str(re.search(r'^(?!.*@(jiweb\.com|ozvid\.com|toxsl\.com)$)[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',request.data.get('email').strip()))    
        if match == "None":
            return Response({"message":"Sorry, registration with this email domain is currently restricted. Please use a different email address.","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(status__in=[ACTIVE,INACTIVE],email=request.data.get('email')).exists():
            return Response({"message":"There is already a registered user with this email.","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(status__in=[ACTIVE,INACTIVE],mobile_no=request.data.get('mobile_no')).exists():
            return Response({"message":"There is already a registered user with this mobile no.","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)

        if not request.data.get('password') == request.data.get('confirm_password'):
            return Response({"message":"Password and Confirm password doesn't match!.","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(
            role_id = CUSTOMER,
            first_name = request.data.get('first_name'),
            last_name = request.data.get('last_name'),
            full_name = request.data.get('first_name')+' '+request.data.get('last_name'),
            email = request.data.get('email'),
            mobile_no = request.data.get('mobile_no'),
            country_code = request.data.get('country_code'),
            country_iso_code = request.data.get('country_iso_code'),
            password = make_password(request.data.get('password')),
            status = ACTIVE,
        )
        try:
            device = Device.objects.get(user = user)
        except Device.DoesNotExist:
            device = Device.objects.create(user = user)
        device.device_type = request.data.get('device_type',ANDROID)
        device.device_name = request.data.get('device_name')
        device.device_token = request.data.get('device_token')
        device.save()
        token, created = Token.objects.get_or_create(user = user)
        data = UserSerializer(user,context = {"request":request}).data
        return Response({"message":f"User registered successfully!","data":data,"status":status.HTTP_200_OK},status=status.HTTP_200_OK)

'''
Verify Otp
'''
class VerifyOTP(APIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = [MultiPartParser,FormParser]

    @swagger_auto_schema(
        tags=["Authentication API's"],
        operation_id="Verify OTP",
        operation_description="Verify OTP",
        manual_parameters=[
            openapi.Parameter('email', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('otp', openapi.IN_FORM, type=openapi.TYPE_STRING),
        ]
    )
    def post(self, request, *args, **kwargs):
        ## validate all required fields 
        response=CustomRequiredFieldsValidator.validate_api_field(self,request,
            [
                {"field_name": "email", "method": "post", "error_message": "Please enter email"},
                {"field_name": "otp", "method": "post", "error_message": "Please enter otp"},
               
            ]
        )
        user = get_or_none(User, "User doesn't exist!", status=ACTIVE, email=request.data.get('email'))
        
        if user.temp_otp == request.data.get('otp'):
            user.temp_otp = ''
            user.is_verified = True
            user.save()
            Token.objects.filter(user=user).delete()
            data = UserSerializer(user,context = {"request":request}).data
            return Response({"message":"OTP Verified Successfully.","data":data,"status":status.HTTP_200_OK},status=status.HTTP_200_OK)
        else:
            return Response({"message":"Incorrect OTP","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)

'''
Resend Verification Link
'''
class ResendVerificationLink(APIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = [MultiPartParser,FormParser]

    @swagger_auto_schema(
        tags=["Authentication API's"],
        operation_id="Resend Verification Link",
        operation_description="Resend Verification Link",
        manual_parameters=[
            openapi.Parameter('email', openapi.IN_FORM, type=openapi.TYPE_STRING),
        ]
    )
    def post(self, request, *args, **kwargs):
        ## validate all required fields 
        response=CustomRequiredFieldsValidator.validate_api_field(self,request,
            [
                {"field_name": "email", "method": "post", "error_message": "Please enter email"},
            ]
        )

        user = get_or_none(User, "User doesn't exist!", status=ACTIVE, email=request.data.get('email'))
        if user.is_verified:
            return Response({"message":"User is already verified!","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        token, created = Token.objects.get_or_create(user = user)
        try:
            OTP = generate_otp()
            user.temp_otp =  OTP
            user.save()
            bulk_send_user_email(request,user,'EmailTemplates/VerifyOTP.html','Account Verification',request.POST.get("email"),token,"",user.temp_otp,"")
            message=f"An verification link has been sent on your email to verify your account."
        except Exception as e:
            db_logger.exception(e)
            message="Something went wrong!"
        return Response({"message":message,"status":status.HTTP_200_OK},status=status.HTTP_200_OK)

'''
Resend Otp
'''
class ResendOTP(APIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = [MultiPartParser,FormParser]

    @swagger_auto_schema(
        tags=["Authentication API's"],
        operation_id="Resend OTP",
        operation_description="Resend OTP",
        manual_parameters=[
            openapi.Parameter('email', openapi.IN_FORM, type=openapi.TYPE_STRING),
        ]
    )
    def post(self, request, *args, **kwargs):
        ## validate all required fields 
        response=CustomRequiredFieldsValidator.validate_api_field(self,request,
            [
                {"field_name": "email", "method": "post", "error_message": "Please enter email"},
            ]
        )

        temp_otp = ''
        message = ''
        user = get_or_none(User, "User doesn't exist!", status=ACTIVE, email=request.data.get('email'))
        try:
            OTP = generate_otp()
            user.temp_otp =  OTP
            user.save()
            temp_otp = OTP
            # send_text_message(f"Enter {OTP} on Dressr AI to verify your account.", to_num )
            if user.email:
                bulk_send_user_email(request,user,'EmailTemplates/OTP_Verification.html','Account Verification',request.POST.get("email"),"","",user.temp_otp,"")
            message=f"An OTP {user.temp_otp} has been sent on your email to verify your account."
        except Exception as e:
            db_logger.exception(e)
            return Response({"message":"Something went wrong!","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message":message,"temp_otp":temp_otp,"status":status.HTTP_200_OK},status=status.HTTP_200_OK)

"""
Check User Email
"""
class CheckUserEmail(APIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = [MultiPartParser,FormParser]

    @swagger_auto_schema(
        tags=["Authentication API's"],
        operation_id="Check User Email",
        operation_description="Check User Email",
        manual_parameters=[
            openapi.Parameter('email', openapi.IN_FORM, type=openapi.TYPE_STRING ,description='Email Address')
        ]
    )
    def post(self, request, *args, **kwargs):
        response=CustomRequiredFieldsValidator.validate_api_field(self,request,
            [
                {"field_name": "email", "method": "post", "error_message": "Please enter email"},
            ]
        )
        if User.objects.filter(status__in=[ACTIVE,INACTIVE],email=request.data.get('email')).exists():
            return Response({"is_exists":True,"status":status.HTTP_200_OK},status=status.HTTP_200_OK)
        else:
            return Response({"is_exists":False,"status":status.HTTP_200_OK},status=status.HTTP_200_OK)

class UserLoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = [MultiPartParser,FormParser]
    @swagger_auto_schema(
        tags=["Authentication API's"],
        operation_id="User Login",
        operation_description="User Login",
        manual_parameters=[
            openapi.Parameter('email', openapi.IN_FORM, type=openapi.TYPE_STRING,description='Email Address'),
            openapi.Parameter('password', openapi.IN_FORM, type=openapi.TYPE_STRING,description='Password'),
            openapi.Parameter('device_type', openapi.IN_FORM, type=openapi.TYPE_NUMBER, description=('1 for Android and 2 for IOS')),
            openapi.Parameter('device_name', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('device_token', openapi.IN_FORM, type=openapi.TYPE_STRING),
        ]
    )
    def post(self, request, *args, **kwargs):
        ## Validate Required Fields
        response=CustomRequiredFieldsValidator.validate_api_field(self,request,
            [
                {"field_name": "email", "method": "post", "error_message": "Please enter email"},
                {"field_name": "password", "method": "post", "error_message": "Please enter password"},
                {"field_name": "device_type", "method": "post", "error_message": "Please enter device type"},
                {"field_name": "device_name", "method": "post", "error_message": "Please enter device name"},
                {"field_name": "device_token", "method": "post", "error_message": "Please enter token"},
            ]
        )
        try:
            user = user_authenticate(email=request.data.get("email").strip(), password=request.data.get("password").strip())
        except:
            create_login_history(request, request.data.get('email'), None, LOGIN_FAILURE, None)
            return Response({"message":"Invalid Login Credentials.", "status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        if not user:
            create_login_history(request,request.data.get('email'),None,LOGIN_FAILURE,None)
            return Response({"message":"Invalid Login Credentials.", "status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        
        if user.status == INACTIVE:
            return Response({"message":"Your account has been inactivated. Please contact admin.","status":status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        
        elif user.status == DELETED:
            return Response({"message":"Your account has been deleted. Please contact admin.","status":status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        
        elif user.status == ACTIVE:
            if user.role_id == ADMIN:
                return Response({"message":"Invalid Login Credentials.","status":status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
            
            ## Manage device data
            device, created = Device.objects.get_or_create(user = user)
            device.device_type = request.data.get('device_type',ANDROID)
            device.device_name = request.data.get('device_name')
            device.device_token = request.data.get('device_token')
            device.save()
            Token.objects.filter(user=user).delete()
            user.save()
            user.refresh_from_db()
            login(request,user)
            create_login_history(request,request.data.get('email'),None,LOGIN_SUCCESS,None)
        data = UserSerializer(user,context = {"request":request}).data
        return Response({"message":"Logged in successfully","data":data,"status":status.HTTP_200_OK}, status=status.HTTP_200_OK)

    

class SocialLogin(APIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = [MultiPartParser,FormParser]

    @swagger_auto_schema(
        tags=["Authentication API's"],
        operation_id="Social Login",
        operation_description="Social Login ",
        manual_parameters=[
            openapi.Parameter('email', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('social_id', openapi.IN_FORM, type=openapi.TYPE_INTEGER),
            openapi.Parameter('social_type', openapi.IN_FORM, type=openapi.TYPE_INTEGER, description=('1:- Google, 2:- Facebook, 3:- Apple, 4:- X, 5:- Linkedin')),
            openapi.Parameter('full_name', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('dob', openapi.IN_FORM, type=openapi.TYPE_STRING,description='Formate : YYYY-MM-DD'),
            openapi.Parameter('gender', openapi.IN_FORM, type=openapi.TYPE_INTEGER,description='MALE : 1 , FEMALE : 2 , OTHER : 3'),
            openapi.Parameter('device_type', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('device_name', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('device_token', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('mobile_device_id', openapi.IN_FORM, type=openapi.TYPE_STRING),
        ],
    )
    def post(self, request, *args, **kwargs):
        ## Validate Required Fields
        response = CustomRequiredFieldsValidator.validate_api_field(self, request, [
            {"field_name": "social_id", "method": "post", "error_message": "Please enter social id"},
            {"field_name": "social_type", "method": "post", "error_message": "Please select social type"},
            {"field_name": "email", "method": "post", "error_message": "Please enter email"},
            {"field_name": "device_type", "method": "post", "error_message": "Please enter device type"},
            {"field_name": "device_name", "method": "post", "error_message": "Please enter device name"},
            {"field_name": "device_token", "method": "post", "error_message": "Please enter device token"},
            {"field_name": "mobile_device_id", "method": "post", "error_message": "Please enter mobile device id"},
        ])

        social_type = request.data.get('social_type')

        if not social_type in ["1","2", "3", "4", "5"]:
            return Response({"message":"Please enter valid choice","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        try:
            email = request.data.get('email')
            # Check if the user already exists with the social_id
            user = User.objects.filter(Q(status=ACTIVE)|Q(status=INACTIVE), email=email).order_by('-created_on').first()
            if user:
                if user.status == INACTIVE:
                    return Response({
                        "message":"Your account has been deactivated. Please contact admin to activate your account.",
                        "status":status.HTTP_400_BAD_REQUEST},
                        status=status.HTTP_400_BAD_REQUEST)
                
                elif user.status == ACTIVE:
                    message = "User logged in successfully"

            else:
                # User does not exist, check if email is already registered
                dob = request.data.get('dob', None)
                if dob:
                    try:
                        dob = datetime.strptime(request.data.get('dob'), "%Y-%m-%d").date()
                    except:
                        return Response({"message":"Please select valid date of birth","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)

                # Create a new user
                user = User.objects.create(
                    email = email ,
                    social_id=request.data.get('social_id'),
                    social_type=social_type,
                    full_name = request.data.get('full_name'),
                    dob = dob,
                    gender = int(request.data.get('gender')) if request.data.get('gender') else None,
                    role_id__in=[CUSTOMER] ,
                    status=ACTIVE,
                    is_verified = True if email else False,
                )

                # send_notification(
                #     created_by = [user],
                #     created_for = None,
                #     title = f"New User Registered",
                #     description =  f"New Customer registered with email {user.email}",
                #     notification_type = ADMIN_NOTIFICATION,
                #     obj_id = str(user.id),
                # )
                ## Mail to admin 
                # admin = User.objects.filter(is_superuser=True,role_id=ADMIN).first()
                # bulk_send_user_email(
                #     request, user, 'EmailTemplates/mail-to-admin.html', 'New User Registered', admin.email,
                #     "", "New User Registered", 'New User Registered', "")
                message = "User created successfully"

            device, _ = Device.objects.get_or_create(user=user)
            device.device_type = request.data.get('device_type')
            device.device_name = request.data.get('device_name')
            device.device_token = request.data.get('device_token')
            device.device_brand = request.data.get('device_brand')
            device.device_model = request.data.get('device_model')
            device.mobile_device_id = request.data.get('mobile_device_id')
            device.save()

            # Manage token
            Token.objects.filter(user=user).delete()
            login(request,user)
            user.save()
            create_login_history(request,email,None,LOGIN_SUCCESS,None)
            data = UserSerializer(user, context={"request": request}).data
            return Response({"message": message, "data": data, "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)
        except Exception as e:
            db_logger.exception(e)
            return Response({"message":"Something went wrong!","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)


class UserCheckView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser,FormParser]

    @swagger_auto_schema(
        tags=["Authentication API's"],
        operation_id="User Check",
        operation_description="User Check",
        manual_parameters=[]
    )
    def get(self, request):
        user = request.user
        data = None
        if user.role_id == CUSTOMER:
            data = UserSerializer(user,context = {"request":request}).data
        return Response({"data":data,"status":status.HTTP_200_OK}, status=status.HTTP_200_OK)


class LogoutView(APIView): 
    permission_classes = (permissions.IsAuthenticated,) 
    parser_classes = [MultiPartParser,FormParser]

    @swagger_auto_schema(
        tags=["Authentication API's"],
        operation_id="Logout",
        operation_description="Logout",
        manual_parameters=[]
    )
    def get(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        logout(request)       
        return Response({"message":"Logout Successfully!","status":status.HTTP_200_OK}, status=status.HTTP_200_OK)


class ForgotPassword(APIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = [MultiPartParser,FormParser]

    @swagger_auto_schema(
        tags=["Authentication API's"],
        operation_id="Forgot Password",
        operation_description="Forgot Password",
        manual_parameters=[
            openapi.Parameter('email', openapi.IN_FORM, type=openapi.TYPE_STRING),
        ],
    )
    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Please enter email"}, status=status.HTTP_400_BAD_REQUEST)

        user = get_or_none(User, "Please enter a registered email address", status=ACTIVE, email=email)
        if not user:
            return Response({"error": "Email not found"}, status=status.HTTP_404_NOT_FOUND)
        token,_ = Token.objects.get_or_create(user=user)
        # Build reset link
        reset_path = reverse("api:reset_password_api")
        reset_link = f"{request.build_absolute_uri(reset_path)}?uid={user.id}&token={token}"
        # Send reset link via email
        bulk_send_user_email(request,user,'EmailTemplates/reset_password.html','Reset Password',email,"","","",reset_link)
        message = f"A password reset link has been sent to {email}."
        return Response({"message": message, "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)


class ForgotPasswordResendLink(APIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = [MultiPartParser,FormParser]

    @swagger_auto_schema(
        tags=["Authentication API's"],
        operation_id="Forgot Password Resend Link",
        operation_description="Forgot Password Resend Link",
        manual_parameters=[
            openapi.Parameter('email', openapi.IN_FORM, type=openapi.TYPE_STRING),
        ]
    )
    def post(self, request, *args, **kwargs):
        response=CustomRequiredFieldsValidator.validate_api_field(self,request,
            [
                {"field_name": "email", "method": "post", "error_message": "Please enter email"},
            ]
        )
        email = request.data.get('email')
        user = get_or_none(User, "User doesn't exist!",status=ACTIVE,email = email)
        token,_ = Token.objects.get_or_create(user=user)
        # Build reset link
        reset_path = reverse("api:reset_password_api")
        reset_link = f"{request.build_absolute_uri(reset_path)}?uid={user.id}&token={token}"
        bulk_send_user_email(request,user,'EmailTemplates/reset_password.html','Reset Password',email,"","","",reset_link)
        message = f"A password reset link has been sent to {email}."
        return Response({"message":message,"temp_otp":user.temp_otp,"status":status.HTTP_200_OK},status=status.HTTP_200_OK)

class ResetPasswordView(APIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = [MultiPartParser,FormParser]

    @swagger_auto_schema(
        tags=["Authentication API's"],
        operation_id="Reset Password",
        operation_description="Reset password using uid and token received via email link",
        manual_parameters=[
            openapi.Parameter('uid', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('token', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('new_password', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('confirm_password', openapi.IN_FORM, type=openapi.TYPE_STRING),
        ],
    )
    def post(self, request, *args, **kwargs):
        uidb64 = request.data.get("uid")
        token = request.data.get("token")
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        if not uidb64 or not token or not new_password:
            return Response({"error": "All fields (uid, token, new_password,confirm_password) are required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            uid = User.objects.get(id=uidb64).id
            user = User.objects.get(id=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Invalid UID"}, status=status.HTTP_400_BAD_REQUEST)

        # Verify token
        if not Token.objects.get(key=token):
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not (request.data.get("new_password") == request.data.get("confirm_password")):
            return Response({"message": "Passwords do not match!","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST) 
        
        if user.check_password(request.data.get("new_password")):
            return Response({"message": "New password should be different from current password.","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        
        # Set new password
        user.password = make_password(new_password)
        user.save()
        Token.objects.filter(user=user).delete()
        logout(request)
        return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)

class ChangePassword(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser,FormParser]

    @swagger_auto_schema(
        tags=["Security Setting API's"],
        operation_id="Change Password",
        operation_description="Change Password",
        manual_parameters=[
            openapi.Parameter('current_password', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('new_password', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('confirm_password', openapi.IN_FORM, type=openapi.TYPE_STRING),
        ]
    )
    def post(self, request, *args, **kwargs):
        ## Validate Required Fields
        response = CustomRequiredFieldsValidator.validate_api_field(self, request, [
            {"field_name": "current_password", "method": "post", "error_message": "Please enter current password"},
            {"field_name": "new_password", "method": "post", "error_message": "Please enter new password"},
            {"field_name": "confirm_password", "method": "post", "error_message": "Please enter confirm password"},
        ])

        user = request.user        
        if not user.check_password(request.data.get("current_password")):
            return Response({"message": "Sorry, you entered incorrect current password", "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST) 
        
        new_password = request.data.get("new_password")
        if new_password == request.data.get("current_password"):
            return Response({"message": "New password should be different from current password.", "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST) 
        
        if new_password != request.data.get("confirm_password"):
            return Response({"message": "Passwords do not match!", "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST) 

        user.password = make_password(request.data.get("new_password"))
        user.save()
        Token.objects.filter(user=user).delete()
        logout(request)
        return Response({"message": "Password updated successfully!", "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)


class DeactivateAccount(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser,FormParser]

    @swagger_auto_schema(
        tags=["Authentication API's"],
        operation_id="Deactivate Account",
        operation_description="Deactivate Account",
        manual_parameters=[]
    )
    def get(self,request):
        user = request.user
        user.status=INACTIVE
        user.save()
        Token.objects.filter(user=user).delete()
        logout(request)
        return Response({"message":"User Account Deactivated successfully!","status":status.HTTP_200_OK},status=status.HTTP_200_OK)

"""
Static Pages
"""
class StaticPages(APIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = [MultiPartParser,FormParser]

    @swagger_auto_schema(
        tags=["Flat Pages"],
        operation_id="Flat Pages Data",
        operation_description="Flat Pages Data",
        manual_parameters=[
            openapi.Parameter('type_id', openapi.IN_FORM, type=openapi.TYPE_INTEGER, description='1 : Terms&Conditions, 2 : PrivacyPolicy, 3 : AboutUs, 4: How it works, 5: Cookie Policy'),
        ],
    )
    def post(self, request, *args, **kwargs):
        if not request.data.get('type_id'):
            return Response({"message": "Please enter page type.","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST) 
        try:
            page = Pages.objects.get(type_id=request.data.get('type_id'),is_active=True)
        except:
            return Response({"data":None, "status":status.HTTP_200_OK},status=status.HTTP_200_OK)
        data = PagesSerializer(page,context = {"request":request}).data
        return Response({"data":data, "status":status.HTTP_200_OK}, status=status.HTTP_200_OK)

"""
Faq Management
"""
class FaqList(APIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = [MultiPartParser,FormParser]

    @swagger_auto_schema(
        tags=["Faq Management"],
        operation_id="Faq's",
        operation_description="Faq's",
        manual_parameters=[
            openapi.Parameter('page',openapi.IN_QUERY,description='page',type=openapi.TYPE_INTEGER),
        ],
    )

    def get(self,request,*args,**kwargs):
        faqs=FAQs.objects.all().order_by("-created_on")
        start,end,meta_data = get_pages_data(request.query_params.get('page', None), faqs)
        data = FaqSeializer(faqs[start : end],many=True,context={"request":request}).data  
        return Response({"data":data,"meta":meta_data,"status":status.HTTP_200_OK},status=status.HTTP_200_OK)

"""
Contact Us
"""
class ContactUsView(APIView):
    permission_classes = [permissions.AllowAny,]
    parser_classes = [MultiPartParser,FormParser]
    @swagger_auto_schema(
        tags=['Contact Us'],
        operation_id="Contact Us",
        operation_description="Contact Us",
        manual_parameters=[
            openapi.Parameter('full_name', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('email', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('mobile_no', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('country_code', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('country_iso_code', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('message', openapi.IN_FORM, type=openapi.TYPE_STRING),
        ],
    )
    def post(self, request, *args, **kwargs):
        ## Validate Required Fields
        response = CustomRequiredFieldsValidator.validate_api_field(self, request, [
            {"field_name": "full_name", "method": "post", "error_message": "Please enter the full name"},
            {"field_name": "email", "method": "post", "error_message": "Please enter the email"},
            {"field_name": "mobile_no", "method": "post", "error_message": "Please enter the mobile number"},
            {"field_name": "country_code", "method": "post", "error_message": "Please enter the country code"},
            {"field_name": "country_iso_code", "method": "post", "error_message": "Please enter the country iso code"},
            {"field_name": "message", "method": "post", "error_message": "Please enter the message"},
        ])

        full_name = request.data.get('full_name')
        email = request.data.get('email')
        message = request.data.get('message')

        try:
            contact_us = ContactUs.objects.get(
                full_name=full_name,
                email=email,
                message=message,
            )
            data = ContactUsSerializer(contact_us,context={"request":request}).data
            return Response(
                {"message": "You have already raised the same query before!", "data": data, "status": status.HTTP_200_OK},
                status=status.HTTP_200_OK)
        except:
            contact_us = ContactUs.objects.create(
                full_name=full_name,
                email=email,
                mobile_no=request.data.get('mobile_no'),
                country_code=request.data.get('country_code'),
                country_iso_code=request.data.get('country_iso_code'),
                message=message,
            )
            data = ContactUsSerializer(contact_us,context={"request":request}).data
            return Response(
                {"message": "Thank you for contacting us. We will get back to you shortly!", "data": data,
                 "status": status.HTTP_200_OK}, status=status.HTTP_200_OK) 

"""
Notification Management
"""
class NotificationsList(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    parser_classes = [MultiPartParser,FormParser]

    @swagger_auto_schema(
        tags=['Notifications'],
        operation_id="Notifications List",
        operation_description="Notifications List",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
        ],
    )
    def get(self, request, *args, **kwargs):
        user = get_or_none(User, "User doesn't exist!", id=request.user.id, role_id=CUSTOMER)
        notifications = Notifications.objects.filter(created_for=user).order_by('-created_on').only('id')
        start,end,meta_data = get_pages_data(request.query_params.get('page', None), notifications.order_by('-created_on'))
        data = NotificationSerializer(notifications.order_by('-created_on')[start : end],many=True,context={"request":request}).data
        return Response({"data":data,"meta":meta_data,"status": status.HTTP_200_OK}, status = status.HTTP_200_OK)


class ClearAllNotifications(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    parser_classes = [MultiPartParser,FormParser]

    @swagger_auto_schema(
        tags=['Notifications'],
        operation_id="Clear All Notifications",
        operation_description="Clear All Notifications",
        manual_parameters=[],
    )
    def delete(self, request, *args, **kwargs):
        notifications = Notifications.objects.filter(created_for=request.user)
        if notifications:
            notifications.delete()
            return Response({"message":"Notifications Deleted Successfully!","status": status.HTTP_200_OK}, status = status.HTTP_200_OK)
        else:
            return Response({"message":"No Notifications to Delete!","status": status.HTTP_200_OK}, status = status.HTTP_200_OK)


class DeleteNotification(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    parser_classes = [MultiPartParser,FormParser]

    @swagger_auto_schema(
        tags=['Notifications'],
        operation_id="Delete Notification",
        operation_description="Delete Notification",
        manual_parameters=[
            openapi.Parameter('notification_id', openapi.IN_QUERY, type=openapi.TYPE_STRING)
        ],
    )
    def delete(self, request, *args, **kwargs):
        ## Validate Required Fields
        response = CustomRequiredFieldsValidator.validate_api_field(self, request, [
            {"field_name": "notification_id", "method": "get", "error_message": "Please enter notification id"},
        ])

        notification = get_or_none(Notifications, "Invalid Notification Id", id=request.query_params.get('notification_id'))
        notification.delete()
        return Response({"message":"Notification Deleted Successfully!","status": status.HTTP_200_OK}, status = status.HTTP_200_OK)


class MarkReadNotificationAPI(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    parser_classes = [MultiPartParser,FormParser]

    @swagger_auto_schema(
        tags=['Notifications'],
        operation_id="Read Notification",
        operation_description="Read Notification",
        manual_parameters=[
            openapi.Parameter('notification_id', openapi.IN_FORM, type=openapi.TYPE_STRING)
        ],
    )
    def post(self, request, *args, **kwargs):
        notification = get_or_none(Notifications, "Invalid Notification Id", id=request.data.get('notification_id'))
        notification.is_read = True
        notification.save()
        return Response({"message":"Notification Marked As Read Successfully!","status": status.HTTP_200_OK}, status = status.HTTP_200_OK)


class UpdateNotificationSettings(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser,FormParser]

    @swagger_auto_schema(
        tags=["Notifications"],
        operation_id="Notification Settings",
        operation_description="Notification Settings",
        manual_parameters=[]
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.notification_enable:
            user.notification_enable = False
            user.save()
            message = "Notification disabled successfully"
        else:
            user.notification_enable = True
            user.save()
            message = "Notification enabled successfully"
        data = UserSerializer(user,context = {"request":request}).data
        return Response({"message":message,"data":data,"status":status.HTTP_200_OK},status=status.HTTP_200_OK)


class UpdateEmailNotificationSettings(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser,FormParser]

    @swagger_auto_schema(
        tags=["Notifications"],
        operation_id="Notification Settings",
        operation_description="Notification Settings",
        manual_parameters=[]
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.email_notification:
            user.email_notification = False
            user.save()
            message = "Email Notifications disabled successfully"
        else:
            user.email_notification = True
            user.save()
            message = "Email Notification enabled successfully"
        data = UserSerializer(user,context = {"request":request}).data
        return Response({"message":message,"data":data,"status":status.HTTP_200_OK},status=status.HTTP_200_OK)

class UserProfileDetails(APIView):
    """
    Profile Management
    """
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser,FormParser]

    @swagger_auto_schema(
        tags=["Profile Management"],
        operation_id="Customer Profile",
        operation_description="Customer Profile",
        manual_parameters=[
            openapi.Parameter('user_id', openapi.IN_QUERY, type=openapi.TYPE_STRING),
        ]
    )
    def get(self, request):
        if request.query_params.get('user_id'):
            user = get_or_none(User, "User doesn't exist!", id=request.query_params.get('user_id'))
        else:
            user = request.user
        data = UserSerializer(user,context = {"request":request}).data
        return Response({"data":data,"status":status.HTTP_200_OK}, status=status.HTTP_200_OK)

class UpdateProfileDetails(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser,FormParser]

    @swagger_auto_schema(
        tags=["Profile Management"],
        operation_id="Update Profile ( Customer )",
        operation_description="Update Profile ( Customer )",
        manual_parameters=[
            openapi.Parameter('first_name', openapi.IN_FORM, type=openapi.TYPE_STRING,description='first name'),
            openapi.Parameter('last_name', openapi.IN_FORM, type=openapi.TYPE_STRING,description='last name'),
            openapi.Parameter('body_type', openapi.IN_FORM, type=openapi.TYPE_STRING,description='1:Slim 2:Athletic 3:Curvy'),
            openapi.Parameter('height', openapi.IN_FORM, type=openapi.TYPE_STRING,description='height in cm'),
            openapi.Parameter('gender', openapi.IN_FORM, type=openapi.TYPE_STRING,description='Male:1 Female:2, Other:3 '),
            openapi.Parameter('skin_tone', openapi.IN_FORM, type=openapi.TYPE_STRING,description='skin tone'),
            openapi.Parameter('hair_color', openapi.IN_FORM, type=openapi.TYPE_STRING,description='hair color'),
            openapi.Parameter('image', openapi.IN_FORM, type=openapi.TYPE_FILE, description="Add Image"),
            openapi.Parameter('others', openapi.IN_FORM, type=openapi.TYPE_STRING,description="to enhance personalization"),
        ],
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        gender = data.get('gender',MALE)
        user_image = request.FILES.get('image',None)
        body_type = data.get('body_type')
        skin_tone = data.get('skin_tone')
        hair_color = data.get('hair_color')
        others = data.get('others')
        hieght_cm = data.get('hieght_cm')
        
        # Update name
        if first_name: user.first_name = first_name
        if last_name: user.last_name = last_name
        
        user.full_name = user.first_name + ' ' + user.last_name

        if gender is not None: user.gender = int(gender)
        if body_type is not None: user.body_type = int(body_type)

        user.skin_tone = skin_tone
        user.hair_color = hair_color
        user.others = others
        user.hieght_cm = hieght_cm
        user.user_image = user_image
        # Profile setup status
        message = "Profile updated successfully!"
        if not user.is_profile_setup:
            user.is_profile_setup = True
            message = "Profile setup completed successfully!"

        user.save()
        serialized_data = UserSerializer(user, context={"request": request}).data
        return Response({"message": message, "data": serialized_data, "status": status.HTTP_200_OK }, status=status.HTTP_200_OK)


"""
App Expiration Date Check
"""
class CheckDate(APIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = [MultiPartParser,FormParser]

    @swagger_auto_schema(
        tags=["Authentication API's"],
        operation_id="Check App Expiration Date",
        operation_description="Check App Expiration Date",
    )

    def get(self, request):
        data={}
        data['datecheck']=RELEASE_DATE
        data['copyrights']="Toxsl Technologies"
        return Response(data)
