
from contact_us.models import *
from static_pages.models import *
from accounts.common_imports import *
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout,login,authenticate
from .serializer import *
from api.helper import *
import re
from urllib.request import urlopen
from tempfile import NamedTemporaryFile
from accounts.models import *
from accounts.utils import *
from wardrobe.models import Wardrobe
from django.core.files.base import ContentFile
from api.avatar import *

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
            openapi.Parameter('username', openapi.IN_FORM, type=openapi.TYPE_STRING ,description='Set Username'),
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
        
        if request.data.get('mobile_no'):
            if User.objects.filter(status__in=[ACTIVE,INACTIVE],mobile_no=request.data.get('mobile_no')).exists():
                return Response({"message":"There is already a registered user with this mobile no.","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)

        if not request.data.get('password') == request.data.get('confirm_password'):
            return Response({"message":"Password and Confirm password doesn't match!.","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        
        if request.data.get('password'):
            check = re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',request.data.get('password'))
            if not check:
                return Response({"message":"Password must contain at least 8 characters, including uppercase, lowercase, numbers, and special characters","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        
        country_code = request.data.get('country_code')
        mobile_no = request.data.get('mobile_no')
        country_iso_code = request.data.get('country_iso_code')
        full_number = f"{country_code}{mobile_no}"

        if request.data.get('mobile_no'):
            if not re.fullmatch(r'^\+[1-9]\d{1,14}$', full_number):
                return Response({"message": "Invalid phone number. Must be in international E.164 format (e.g., +14151234567).","status": status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        
        email_first = request.data.get('email').split('@')
        email_first = email_first[0]
        username  = request.data.get('username')
        if not username:
            suggestions = generate_mydressr_username(email_first)
            username = suggestions[0]

        if User.objects.filter(username=username).exists():
            suggestions = generate_mydressr_username(email_first)
            return Response({"message": "Username already taken.","suggestions": suggestions,"status": 400}, status=400)

        user = User.objects.create(
            role_id = CUSTOMER,
            username=username,
            first_name = request.data.get('first_name'),
            last_name = request.data.get('last_name'),
            full_name = request.data.get('first_name')+' '+request.data.get('last_name'),
            email = request.data.get('email'),
            mobile_no=mobile_no,
            country_code=country_code,
            country_iso_code=country_iso_code,
            password = make_password(request.data.get('password')),
            status = ACTIVE,
        )

        if not user.is_plan_purchased:
            try:
                plan=SubscriptionPlans.objects.filter(is_free_plan=True).first()
            except:
                return Response({"message":"Subscription plan not found!","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
            
            is_valid_purchse = is_first_time_subscription_purchase(user)
            if not is_valid_purchse['is_valid']:
                return Response({"message":is_valid_purchse['message'],"status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
            
            purchased_plan = UserPlanPurchased.objects.create(
                plan_id=generate_plan_id(),
                subscription_plan = plan,
                purchased_by = user,
                status = USER_PLAN_IN_QUEUE,
                amount = plan.price,
                final_amount = plan.final_price,
                features = plan.features,
                month_year = plan.month_year,
                validity = plan.validity,
            )
            activate_subscription(user)
            user.save()
        wardrobe,_ = Wardrobe.objects.get_or_create(user=user)
        try:
            device = Device.objects.get(user = user)
        except Device.DoesNotExist:
            device = Device.objects.create(user = user)
        device.device_type = request.data.get('device_type')
        device.device_name = request.data.get('device_name')
        device.device_token = request.data.get('device_token')
        device.save()
        token, created = Token.objects.get_or_create(user = user)
        data = UserSerializer(user,context = {"request":request}).data
        # send notification to admin
        send_notification(
            created_by=user,
            created_for=None,
            title=f"New Customer Registered",
            description=f"New Customer registered with email {user.email}",
            notification_type=ADMIN_NOTIFICATION,
            obj_id=str(user.id),
        )
        bulk_send_user_email(request,user,'EmailTemplates/registration-success.html','Welcome To Dressr',request.data.get("email"),"","","","",assign_to_celery=False)
        return Response({"message":f"User registered successfully!","data":data,"status":status.HTTP_200_OK},status=status.HTTP_200_OK)

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
            openapi.Parameter('username', openapi.IN_FORM, type=openapi.TYPE_STRING,description='Username'),
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
                {"field_name": "password", "method": "post", "error_message": "Please enter password"},
                {"field_name": "device_type", "method": "post", "error_message": "Please enter device type"},
                {"field_name": "device_name", "method": "post", "error_message": "Please enter device name"},
                {"field_name": "device_token", "method": "post", "error_message": "Please enter token"},
            ]
        )
        identifier = request.data.get("username", "").strip() or request.data.get("email", "").strip()
        if not identifier:
            return Response({"message": "Please provide either username or email.", "status": status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        try:
            user = user_authenticate(identifier, request.data.get("password", "").strip())
            if not user:
                return Response({"message": "Invalid login credentials.", "status": status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        except :
            return Response({"message": "Invalid login credentials.", "status": status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)

        if user.status == INACTIVE:
            return Response({"message":"Your account has been inactivated. Please contact admin.","status":status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        
        elif user.status == DELETED:
            return Response({"message":"Your account has been deleted. Please contact admin.","status":status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
        
        elif user.status == ACTIVE:
            if user.role_id == ADMIN:
                return Response({"message":"Invalid Login Credentials.","status":status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
            wardrobe,_ = Wardrobe.objects.get_or_create(user=user)
            ## Manage device data
            device, created = Device.objects.get_or_create(user = user)
            device.device_type = request.data.get('device_type')
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
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["Authentication API's"],
        operation_id="Social Login",
        operation_description="Social Login ",
        manual_parameters=[
            openapi.Parameter('email', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('profile_pic', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('full_name', openapi.IN_FORM, type=openapi.TYPE_STRING),
            #Social Id fields
            openapi.Parameter('social_id', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('social_type', openapi.IN_FORM, type=openapi.TYPE_INTEGER,description=('1:GOOGLE, 2:FACEBOOK, 3:APPLE')),
            
            openapi.Parameter('device_type', openapi.IN_FORM, type=openapi.TYPE_NUMBER, description=('1 for Android and 2 for IOS')),
            openapi.Parameter('device_name', openapi.IN_FORM, type=openapi.TYPE_STRING),
            openapi.Parameter('device_token', openapi.IN_FORM, type=openapi.TYPE_STRING)
        ],
    )
    def post(self, request, *args, **kwargs):
        ## Validate Required Fields
        required_fields = list(filter(None, [
            RequiredFieldValidations.validate_field(self,request,'email',"post","Please enter email"),
            
            RequiredFieldValidations.validate_field(self,request,'social_id',"post","Please enter social id"),
            RequiredFieldValidations.validate_field(self,request,'social_type',"post","Please enter social type"),

            RequiredFieldValidations.validate_field(self,request,'device_type',"post","Please enter device type"),
            RequiredFieldValidations.validate_field(self,request,'device_name',"post","Please enter device name"),
            RequiredFieldValidations.validate_field(self,request,'device_token',"post","Please enter device token"),
        ]))
        all_users = User.objects.filter(social_id__isnull=False, status__in=[ACTIVE,INACTIVE]).values_list("social_id",flat=True)
        socialidList = [i for i in all_users]
        if request.data.get('social_id') in socialidList:
            user = User.objects.filter(social_id=request.data.get('social_id')).order_by('created_on').last()
            if user.status == INACTIVE:
                return Response({"message":"Your account has been deactivated. Please contact admin to activate your account.","status":status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
            elif user.status == DELETED:
                return Response({"message":"Your account has been deleted. Please contact admin.","status":status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
            elif user.status == ACTIVE:
                try:
                    user = user_authenticate(request.data.get('email'),request.data.get('social_id'))
                except:
                    return Response({"message":"Invalid Login Credentials.", "status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
                
                if request.data.get("profile_pic"):
                    img_temp = NamedTemporaryFile(delete = True)
                    img_temp.write(urlopen(request.data.get("profile_pic")).read())
                    img_temp.flush()
                    user.profile_pic.save(f"image_{user.id}", File(img_temp))
                user.save()
                message = "Logged in successfully!"
        elif User.objects.filter(status = ACTIVE, email = request.data.get('email')):
            user = User.objects.filter(status = ACTIVE, email = request.data.get('email')).order_by('created_on').last()
            backend='accounts.backend.EmailLoginBackend'
            login(request,user,backend=backend)
            if request.data.get("profile_pic"):
                img_temp = NamedTemporaryFile(delete = True)
                img_temp.write(urlopen(request.data.get("profile_pic")).read())
                img_temp.flush()
                user.profile_pic.save("image_%s" % user.pk, File(img_temp))
            user.save()
            message = "Logged in successfully!"
        else:
            if request.data.get("email"):
                if User.objects.filter(Q(status=ACTIVE)|Q(status=INACTIVE),email=request.data.get("email")):
                    return Response({"message":"There is already a registered user with this email id.","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)

            if request.data.get("social_id"):
                if User.objects.filter(Q(status=ACTIVE)|Q(status=INACTIVE),social_id=request.data.get("social_id")):
                    return Response({"message":"There is already a registered user with this social_id.","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
            
            user = User.objects.create(
                email = request.data.get("email"),
                social_id = request.data.get('social_id'),
                social_type = request.data.get('social_type'),
                password=make_password(request.data.get('social_id')),
                role_id = CUSTOMER,
                status=ACTIVE
            )
            # wallet = get_user_wallet(user)
            if request.data.get("full_name"):
                user.name = request.data.get("full_name")

            if request.data.get("profile_pic"):
                img_temp = NamedTemporaryFile(delete = True)
                img_temp.write(urlopen(request.data.get("profile_pic")).read())
                img_temp.flush()
                user.profile_pic.save("image_%s" % user.pk, File(img_temp))
            user.save()
            message="Logged in successfully!"
            # send notification to admin
            send_notification(
                created_by=user,
                created_for=None,
                title=f"New Customer Registered",
                description=f"New Customer registered with email {user.email}",
                notification_type=ADMIN_NOTIFICATION,
                obj_id=str(user.id),
            )
            bulk_send_user_email(request,user,'EmailTemplates/registration-success.html','Welcome To Dressr',request.POST.get("email"),"","","","",assign_to_celery=False)
        try:
            device = Device.objects.get(created_by = user)
        except Device.DoesNotExist:
            device = Device.objects.create(created_by = user)
        device.device_type = request.data['device_type']
        device.device_name = request.data['device_name']
        device.device_token = request.data['device_token']
        device.save()
        token, created = Token.objects.get_or_create(user = user)

        data = UserSerializer(user,context = {"request":request}).data
        return Response({"data":data,"message":message, "url":request.path},status=status.HTTP_200_OK)

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
        response=CustomRequiredFieldsValidator.validate_api_field(self,request,
            [
                {"field_name": "email", "method": "post", "error_message": "Please enter email"},
            ]
        )
        email = request.data.get("email").strip()
        if not email:
            return Response({"error": "Please enter email"}, status=status.HTTP_400_BAD_REQUEST)
        user = get_or_none(User, "Please enter a registered email address", status=ACTIVE, email=email)
        if not user:
            return Response({"error": "Email not found"}, status=status.HTTP_404_NOT_FOUND)
        token,_ = Token.objects.get_or_create(user=user)
        # Build reset link
        reset_path = reverse("accounts:reset_password_user", kwargs={"uid": user.id, "token": token})
        reset_link = request.build_absolute_uri(reset_path)
        # Send reset link via email
        bulk_send_user_email(request,user,'EmailTemplates/ResetPassword.html','Reset Your Password',email,reset_link,"","","","","","",assign_to_celery=False)
        message = f"A password reset link has been sent to {email}."
        return Response({"message": message,"status": status.HTTP_200_OK}, status=status.HTTP_200_OK)

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
        email = request.data.get("email").strip()
        if not email:
            return Response({"error": "Please enter email"}, status=status.HTTP_400_BAD_REQUEST)
        user = get_or_none(User, "Please enter a registered email address", status=ACTIVE, email=email)
        if not user:
            return Response({"error": "Email not found"}, status=status.HTTP_404_NOT_FOUND)
        token,_ = Token.objects.get_or_create(user=user)
        reset_path = reverse("accounts:reset_password_user", kwargs={"uid": user.id, "token": token})
        reset_link = request.build_absolute_uri(reset_path)
        bulk_send_user_email(request,user,'EmailTemplates/ResetPassword.html','Reset Your Password',email,reset_link,"","","","","","",assign_to_celery=False)
        message = f"A password reset link has been sent to {email}."
        return Response({"message": message,"status": status.HTTP_200_OK}, status=status.HTTP_200_OK)

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
        
        if request.data.get('new_password'):
            check = re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',request.data.get('new_password'))
            if not check:
                return Response({"message":"Password must contain at least 8 characters, including uppercase, lowercase, numbers, and special characters","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
            
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
        if new_password:
            check = re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',new_password)
            if not check:
                return Response({"message":"Password must contain at least 8 characters, including uppercase, lowercase, numbers, and special characters","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
            
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
            openapi.Parameter('type_id', openapi.IN_FORM, type=openapi.TYPE_INTEGER, description='1 : Terms&Conditions, 2 : PrivacyPolicy, 3 : AboutUs, 4: How it works'),
        ],
    )
    def post(self, request, *args, **kwargs):
        if not request.data.get('type_id'):
            return Response({"message": "Please enter page type.","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST) 
        try:
            page = Pages.objects.get(type_id=request.data.get('type_id'),is_active=True)
        except:
            return Response({"data":[], "status":status.HTTP_200_OK},status=status.HTTP_200_OK)
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
        country_code = request.data.get('country_code')
        mobile_no = request.data.get('mobile_no')
        country_iso_code = request.data.get('country_iso_code')
        full_number = f"{country_code}{mobile_no}"

        if not re.fullmatch(r'^\+[1-9]\d{1,14}$', full_number):
            return Response({"message": "Invalid phone number. Must be in international E.164 format (e.g., +14151234567).","status": status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)

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
                mobile_no=mobile_no,
                country_code=country_code,
                country_iso_code=country_iso_code,
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
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        tags=["Profile Management"],
        operation_id="Customer Profile",
        operation_description="Customer Profile",
        manual_parameters=[
            openapi.Parameter('user_id', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('username', openapi.IN_QUERY, type=openapi.TYPE_STRING),
        ]
    )
    def get(self, request):

        user_id = request.query_params.get("user_id")
        username = request.query_params.get("username")
        if user_id or username:
            query = Q()
            if user_id:
                query |= Q(id=user_id)
            if username:
                query |= Q(username=username)
            user = User.objects.filter(query).first()
            if not user:
                return Response({"message": "User does not exist!", "status": status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        else:
            user = request.user
        data = UserSerializer(user, context={"request": request}).data
        return Response({"data": data, "status": status.HTTP_200_OK}, status=status.HTTP_200_OK)


class UpdateProfileDetails(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser,FormParser]

    @swagger_auto_schema(
        tags=["Profile Management"],
        operation_id="Update Profile ( Customer )",
        operation_description="Update Profile ( Customer )",
        manual_parameters=[
            openapi.Parameter('username', openapi.IN_FORM, type=openapi.TYPE_STRING,description='username'),
            openapi.Parameter('dob', openapi.IN_FORM, type=openapi.TYPE_STRING,description='Date of birth'),
            openapi.Parameter('first_name', openapi.IN_FORM, type=openapi.TYPE_STRING,description='first name'),
            openapi.Parameter('last_name', openapi.IN_FORM, type=openapi.TYPE_STRING,description='last name'),
            openapi.Parameter('body_type', openapi.IN_FORM, type=openapi.TYPE_STRING,description='body type id'),
            openapi.Parameter('profile_pic', openapi.IN_FORM, type=openapi.TYPE_FILE, description="Add profile pic image"),
            openapi.Parameter('height', openapi.IN_FORM, type=openapi.TYPE_STRING,description='height in cm'),
            openapi.Parameter('gender', openapi.IN_FORM, type=openapi.TYPE_STRING,description='Male:1 Female:2, Other:3 '),
            openapi.Parameter('skin_tone_id', openapi.IN_FORM, type=openapi.TYPE_STRING,description='skin tone id'),
            openapi.Parameter('hair_color_id', openapi.IN_FORM, type=openapi.TYPE_STRING,description='hair color id'),
            openapi.Parameter('image', openapi.IN_FORM, type=openapi.TYPE_FILE, description="Add Image"),
            openapi.Parameter('others', openapi.IN_FORM, type=openapi.TYPE_STRING,description="to enhance personalization"),
        ],
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        gender = data.get('gender')
        profile_pic = request.FILES.get('profile_pic')
        others = data.get('others')
        hieght_cm = data.get('height')
        dob = data.get('dob')

        if first_name: user.first_name = first_name
        if last_name: user.last_name = last_name
        
        user.full_name = user.first_name + ' ' + user.last_name

        if gender is not None: user.gender = int(gender)

        if data.get('body_type'):
            body_type = BodyType.objects.filter(id = data.get('body_type')).first()
            if body_type:
                user.body_type = body_type
            else:
                return Response({"message":"Body type not found !","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
            
        if data.get('skin_tone_id'):
            skin_tone = SkinTone.objects.filter(id=data.get('skin_tone_id')).first()
            if skin_tone:
                user.skin_tone = skin_tone
            else:
                return Response({"message": "Skin tone not found!", "status": status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)

        if data.get('hair_color_id'):
            hair_color = HairColor.objects.filter(id=data.get('hair_color_id')).first()
            if hair_color:
                user.hair_color = hair_color
            else:
                return Response({"message": "Hair colour not found!", "status": status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
            
        if request.data.get('username'):
            new_username = request.data.get('username').strip()
            if User.objects.filter(username=new_username).exclude(id=user.id).exists():
                suggestions = generate_mydressr_username(user.full_name)
                return Response({"message": "Username already taken.",
                    "suggestions": suggestions,
                    "status": 400
                }, status=400)

            formatted_suggestions = generate_mydressr_username(new_username)
            final_username = formatted_suggestions[0]
            user.username = final_username
            
        if request.data.get('dob'):
            user.dob = dob
            
        user.others = others
        user.hieght_cm = hieght_cm

        uploaded = request.FILES.get("image")
        user.user_image = uploaded
        user.save()
        
        # if uploaded:
        #     user.refresh_from_db()
        #     avatar_url = request.build_absolute_uri(user.user_image.url)
        #     db_logger.info(avatar_url)
        #     prompt = (
        #         "Create a high-resolution avatar version of the person in the image. Do not change or modify the clothing, background, body, pose, lighting, or any other part of the image. Only transform the face into a realistic, natural-looking avatar while preserving the original facial structure, skin tone, and hair style as closely as possible. The output must look almost identical to the original photo except for the face being converted into an avatar style."
        #     )
        #     result = create_lightx_avatar(avatar_url, avatar_url, prompt=prompt)
        #     if not result.get("success"):
        #         return Response(
        #             {"message": "Avatar generation failed", "error": result.get("error")},
        #             status=400
        #         )
        #     order_id = result["data"]["body"]["orderId"]
        #     max_attempts = 10
        #     wait_time = 3
        #     avatar_result = None

        #     for attempt in range(max_attempts):
        #         time.sleep(wait_time)

        #         status_check = check_lightx_order_status(order_id)
        #         if not status_check.get("success"):
        #             return Response(
        #                 {"message": "Order status failed", "error": status_check.get("error")},
        #                 status=400
        #             )

        #         body = status_check["data"]["body"]
        #         status_data = body.get("status")
        #         output = body.get("output")

        #         if output and status_data in ["active", "success"]:
        #             avatar_result = status_check
        #             break

        #         if status_data in ["failed", "error"]:
        #             return Response(
        #                 {"message": "Avatar generation failed", "details": body},
        #                 status=400
        #             )
        #     if not avatar_result:
        #         return Response(
        #             {"message": "Avatar is still processing. Try again after a few seconds."},
        #             status=202
        #         )
        #     image_url = avatar_result["data"]["body"]["output"]
        #     img_response = requests.get(image_url)
        #     if img_response.status_code != 200:
        #         return Response({"message": "Failed to download avatar image"}, status=400)

        #     file_name = image_url.split("/")[-1]
        #     user.user_image.save(file_name, ContentFile(img_response.content))
        #     user.save()
        #     send_notification(
        #         created_by=user,
        #         created_for=None,
        #         title="New Avatar Generated",
        #         description=f"A new avatar has been successfully generated for {user.full_name}.",
        #         notification_type=ADMIN_NOTIFICATION,
        #         obj_id=str(user.id),
        #     )
        if request.FILES.get('profile_pic'):
            user.profile_pic = profile_pic
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
        data['copyrights']="My Dressr"
        return Response(data)

class SkinToneListView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser,FormParser]

    @swagger_auto_schema(
        tags=["Profile Management"],
        operation_id="Skin Tone List",
        operation_description="Skin Tone List",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
        ]
    )
    def get(self, request, *args, **kwargs):
        skin_tone = SkinTone.objects.filter(is_active=True).order_by("-created_on")
        start,end,meta_data = get_pages_data(request.query_params.get('page', None),skin_tone)
        data = SkinToneSerializer(skin_tone[start : end],many=True,context={"request":request}).data
        return Response({"data":data,"meta":meta_data,"status": status.HTTP_200_OK}, status = status.HTTP_200_OK)

class HairColorListView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser,FormParser]

    @swagger_auto_schema(
        tags=["Profile Management"],
        operation_id="Hair Colour List",
        operation_description="Hair Colour List",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
        ]
    )
    def get(self, request, *args, **kwargs):
        hair_color = HairColor.objects.filter(is_active=True).order_by("-created_on")
        start,end,meta_data = get_pages_data(request.query_params.get('page', None),hair_color)
        data = SkinToneSerializer(hair_color[start : end],many=True,context={"request":request}).data
        return Response({"data":data,"meta":meta_data,"status": status.HTTP_200_OK}, status = status.HTTP_200_OK)

class BodyTypeListView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser,FormParser]

    @swagger_auto_schema(
        tags=["Profile Management"],
        operation_id="Body Type List",
        operation_description="Body Type List",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, type=openapi.TYPE_INTEGER)
        ]
    )
    def get(self, request, *args, **kwargs):
        body_type = BodyType.objects.filter(is_active=True).order_by("-created_on")
        start,end,meta_data = get_pages_data(request.query_params.get('page', None),body_type)
        data = BodyTypeSerializer(body_type[start : end],many=True,context={"request":request}).data
        return Response({"data":data,"meta":meta_data,"status": status.HTTP_200_OK}, status = status.HTTP_200_OK)
    

#---------------AI avatar creation API-----------------


class CreateUserAvatarAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser,FormParser]

    @swagger_auto_schema(
        tags=["User Avatar Management"],
        operation_id="Create User Avatar",
        operation_description="Create User Avatar",
        manual_parameters=[
            
            openapi.Parameter('body_type', openapi.IN_FORM, type=openapi.TYPE_STRING,description='body type id'),
            openapi.Parameter('height', openapi.IN_FORM, type=openapi.TYPE_STRING,description='height in cm'),
            openapi.Parameter('skin_tone_id', openapi.IN_FORM, type=openapi.TYPE_STRING,description='skin tone id'),
            openapi.Parameter('hair_color_id', openapi.IN_FORM, type=openapi.TYPE_STRING,description='hair color id'),
            openapi.Parameter('image', openapi.IN_FORM, type=openapi.TYPE_FILE, description="Add Image"),
           
        ],
    )
    def post(self, request, *args, **kwargs):
        response=CustomRequiredFieldsValidator.validate_api_field(self,request,
            [
                {"field_name": "body_type", "method": "post", "error_message": "Please enter body type"},
                {"field_name": "skin_tone_id", "method": "post", "error_message": "Please enter skin tone"},
                {"field_name": "hair_color_id", "method": "post", "error_message": "Please enter hair colour"},
                {"field_name": "height", "method": "post", "error_message": "Please enter height"},
                {"field_name": "image", "method": "post", "error_message": "Please upload image"},
               
            ]
        )

        user = request.user
        data = request.data
        height_cm = data.get('height')
        # Fetch objects in a cleaner way
        body_type = BodyType.objects.filter(id=data.get("body_type")).first()
        skin_tone = SkinTone.objects.filter(id=data.get("skin_tone_id")).first()
        hair_color = HairColor.objects.filter(id=data.get("hair_color_id")).first()

        # Validate these 3 objects
        if not body_type:
            return Response({"message": "Body type not found!", "status": 400}, status=400)

        if not skin_tone:
            return Response({"message": "Skin tone not found!", "status": 400}, status=400)

        if not hair_color:
            return Response({"message": "Hair color not found!", "status": 400}, status=400)

        # Upload image
        uploaded_image = request.FILES.get("image")
        user.user_image = uploaded_image
        user.save()

        if uploaded_image:
            user.refresh_from_db()
            avatar_url = request.build_absolute_uri(user.user_image.url)
            db_logger.info(avatar_url)

            # Prepare prompt
            prompt = (
                f"Create a high-resolution avatar version of the person in the image. "
                f"The person has the following characteristics: "
                f"body type = '{body_type.title}', "
                f"skin tone = '{skin_tone.title}', "
                f"hair color = '{hair_color.title}', "
                f"height = {height_cm} cm. "
                f"Do NOT change or modify the clothing, background, body, body shape, height, pose, or lighting. "
                f"ONLY transform the face into a realistic, natural-looking avatar while preserving the original "
                f"facial structure, skin tone appearance, and hairstyle. "
                f"The output must look almost identical to the original photo except for the face being converted "
                f"into a natural avatar style."
            )

            result = create_lightx_avatar(avatar_url, avatar_url, prompt=prompt)

            if not result.get("success"):
                return Response(
                    {"message": "Avatar generation failed", "error": result.get("error")},
                    status=400
                )

            order_id = result["data"]["body"]["orderId"]

            # Polling Loop
            max_attempts = 10
            wait_time = 3
            avatar_result = None

            for _ in range(max_attempts):
                time.sleep(wait_time)

                status_check = check_lightx_order_status(order_id)

                if not status_check.get("success"):
                    return Response(
                        {"message": "Order status failed", "error": status_check.get("error")},
                        status=400
                    )

                body = status_check["data"]["body"]
                status_data = body.get("status")
                output = body.get("output")

                if output and status_data in ["active", "success"]:
                    avatar_result = status_check
                    break

                if status_data in ["failed", "error"]:
                    return Response(
                        {"message": "Avatar generation failed", "details": body},
                        status=400
                    )

            if not avatar_result:
                return Response(
                    {"message": "Avatar is still processing. Try again shortly."},
                    status=202
                )

            # Download generated image
            image_url = avatar_result["data"]["body"]["output"]
            img_response = requests.get(image_url)

            if img_response.status_code != 200:
                return Response({"message": "Failed to download avatar image"}, status=400)

            file_name = image_url.split("/")[-1]
            user.user_image.save(file_name, ContentFile(img_response.content))
            user.save()

            # Send notification
            send_notification(
                created_by=user,
                created_for=None,
                title="New Avatar Generated",
                description=f"A new avatar has been successfully generated for {user.full_name}.",
                notification_type=ADMIN_NOTIFICATION,
                obj_id=str(user.id),
            )

        serialized_data = UserSerializer(user, context={"request": request}).data
        return Response(
            {"message": "Avatar created successfully!", "data": serialized_data, "status": 200},
            status=200
        )

class CreateVirtualTryOnAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        tags=["Virtual Try On Management"],
        operation_id="Create Virtual Try On",
        operation_description="Create Virtual Try On",
        manual_parameters=[
            openapi.Parameter('sigment_type', openapi.IN_FORM, type=openapi.TYPE_INTEGER,description='0:upper_body, 1:lower_body, 2:full_body'),
            openapi.Parameter('garment_image', openapi.IN_FORM, type=openapi.TYPE_FILE,description='upload garment image'),
        ],
    )
    def post(self, request, *args, **kwargs):
        response = CustomRequiredFieldsValidator.validate_api_field(
            self, request,
            [
                {"field_name": "sigment_type", "method": "post", "error_message": "Please enter sigment type"},
                {"field_name": "garment_image", "method": "post", "error_message": "Please upload garment image"},
            ]
        )

        user = request.user
        garment_file = request.FILES.get("garment_image")
        sig_type = int(request.data.get("sigment_type"))
        avatar_url = request.build_absolute_uri(user.user_image.url)
        existing_tryon = VirtualTryOn.objects.filter(user=user,sigmentation_type=sig_type,garment_image__icontains=garment_file.name,source_image=user.user_image).first()

        if existing_tryon and existing_tryon.output_image:
            serialized_data = VirtualTryOnSerializer(existing_tryon, context={"request": request}).data
            return Response({"message": "Existing Virtual Try On Found!","data": serialized_data,"status": 200}, status=200)

        virtual_try_on = VirtualTryOn.objects.create(
            user=user,
            sigmentation_type=sig_type,
            garment_image=garment_file,
            source_image=user.user_image,
            status=TRY_ON_PROCESSING
        )

        garment_url = request.build_absolute_uri(virtual_try_on.garment_image.url)
        result = lightx_virtual_tryon(avatar_url, garment_url, sig_type)
        if not result.get("success"):
            virtual_try_on.status = TRY_ON_FAILED
            virtual_try_on.save()
            return Response({"message": "Virtual try on failed", "error": result.get("error")}, status=400)

        order_id = result["data"]["body"]["orderId"]
        virtual_try_on.order_id = order_id
        virtual_try_on.save()

        max_attempts = 10
        wait_time = 3
        avatar_result = None

        for _ in range(max_attempts):
            time.sleep(wait_time)

            status_check = check_virtual_tryon_status(order_id)
            if not status_check.get("success"):
                return Response({"message": "Order status failed", "error": status_check.get("error")}, status=400)

            body = status_check["data"]["body"]
            status_data = body.get("status")
            output = body.get("output")

            if output and status_data in ["active", "success"]:
                avatar_result = status_check
                break

            if status_data in ["failed", "error"]:
                virtual_try_on.status = "failed"
                virtual_try_on.save()
                return Response({"message": "Virtual try on generation failed", "details": body}, status=400)

        if not avatar_result:
            return Response({"message": "Virtual try on still processing. Try again later."}, status=202)

        image_url = avatar_result["data"]["body"]["output"]
        img_response = requests.get(image_url)

        if img_response.status_code != 200:
            return Response({"message": "Failed to download virtual try on image"}, status=400)

        file_name = image_url.split("/")[-1]
        virtual_try_on.output_image.save(file_name, ContentFile(img_response.content))
        virtual_try_on.status = TRY_ON_SUCCESS
        virtual_try_on.save()

        send_notification(
            created_by=user,
            created_for=None,
            title="New Virtual Try On Generated",
            description=f"A new virtual try on is ready for {virtual_try_on.user.full_name}.",
            notification_type=ADMIN_NOTIFICATION,
            obj_id=str(virtual_try_on.user.id),
        )
        serialized_data = VirtualTryOnSerializer(virtual_try_on, context={"request": request}).data
        return Response({"message": "Virtual Try On Generated Successfully!","data": serialized_data,"status": 200}, status=200)
