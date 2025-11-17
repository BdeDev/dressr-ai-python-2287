from api.views_authentication import *
from subscription.models import *
from .serializer import *
from accounts.stripe_views import *

"""
User Stripe Cards API
"""

class AddStripeCardAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser,FormParser]

    @swagger_auto_schema(
        tags=["Stripe Card Management"],
        operation_id="Add Stripe Card ",
        operation_description="Add Stripe Card",
        manual_parameters=[
            openapi.Parameter('card_token', openapi.IN_FORM, type=openapi.TYPE_STRING,description="card_token")
        ]
    )
    def post(self, request, *args, **kwargs):
        ## validate all required fields 
        response = CustomRequiredFieldsValidator.validate_api_field(self, request, [
            {"field_name": "card_token", "method": "post", "error_message": "Please enter card token"},
        ])
        try:
            check_duplicate = CheckDuplicateCard(
                user = request.user,
                card_token=request.data.get('card_token').strip()
            )
            if check_duplicate[0]:
                return Response({"message":"Sorry this card is already linked with your account or something went wrong please try again later","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST) 
            else:
                create_card=CreateStripeCard(request.user,request.data.get('card_token').strip())
                if create_card:
                    return Response({"message":"Card added successfully!","status": status.HTTP_200_OK}, status = status.HTTP_200_OK) 
                else:
                    return Response({"message":"Sorry,something went wrong please try again later.","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST) 
        except:
            return Response({"message":"Please enter valid card details","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)

class StripeAllUserCards(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser,FormParser]
    @swagger_auto_schema(
        tags=["Stripe Card Management"],
        operation_id="All Stripe Cards List ",
        operation_description="All Stripe Cards List",
        manual_parameters=[]
    )
    def get(self, request, *args, **kwargs):
        try:
            set_stripe_keys()
            cards = stripe.Customer.list_sources(request.user.customer_id,object="card",limit=15)
            customer = stripe.Customer.retrieve(request.user.customer_id)
            data = []
            for card in cards.data:
                data.append({
                    "id":card.id,
                    "brand":card.brand,
                    "country":card.country,
                    "customer":card.customer,
                    "cvc_check":card.cvc_check,
                    "exp_month":card.exp_month,
                    "exp_year":card.exp_year,
                    "last4":card.last4,
                    "name":card.name,
                    "default": True if customer.default_source == card.id else False,
                })
            return Response({"data":data,"status":status.HTTP_200_OK},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message":"data not found!","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)      

class DeleteStripeCardAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser,FormParser]
    @swagger_auto_schema(
        tags=["Stripe Card Management"],
        operation_id="Delete Stripe Card by ID ",
        operation_description="Delete Stripe Card by ID ",
        manual_parameters=[
            openapi.Parameter('card_id', openapi.IN_QUERY, type=openapi.TYPE_STRING),
        ]
    )
    def get(self, request, *args, **kwargs):
        ## validate all required fields 
        response = CustomRequiredFieldsValidator.validate_api_field(self, request, [
            {"field_name": "card_id", "method": "get", "error_message": "Please enter card id"},
        ])
        try:
            card_id = request.query_params.get('card_id')
            card_deleted = DeleteStripeCard(
                user = request.user ,
                card_id = card_id
            )
            if card_deleted:
                return Response({"message":"Card Removed successfully!","status": status.HTTP_200_OK}, status = status.HTTP_200_OK)    
            else:
                return Response({"message":"Please enter valid card id!","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message":"Please enter valid card id","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)

"""
Subscriptions List
"""
class SubscriptionPlansListing(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["Subscriptions"],
        operation_id="subscription_list",
        operation_description="Subscription List",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY,description="page",type=openapi.TYPE_INTEGER),
        ],
    )
    def get(self, request, *args, **kwargs):
        subscriptions=SubscriptionPlans.objects.filter(status=True,is_deleted = False).order_by('-created_on')
        start,end,meta_data = get_pages_data(request.query_params.get('page') if request.query_params.get('page') else None, subscriptions)
        data = SubscriptionSerializer(subscriptions[start : end],many=True,context = {"request":request}).data
        return Response({"data":data,"meta":meta_data,"status":status.HTTP_200_OK},status=status.HTTP_200_OK)


class MyPurchasedPlansList(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["Subscriptions"],
        operation_id="my_plans_list",
        operation_description="My Plans List",
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY,description="page",type=openapi.TYPE_INTEGER),
        ],
    )
    def get(self, request, *args, **kwargs):
        try:
            user=User.objects.get(id=request.user.id,role_id=CUSTOMER)
        except:
            return Response({"message":"User does not exists!","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        plans=UserPlanPurchased.objects.filter(purchased_by=user).order_by('-created_on')
        start,end,meta_data = get_pages_data(request.query_params.get('page') if request.query_params.get('page') else None, plans)
        data = PurchasedPlanListingSerializer(plans[start : end],many=True,context = {"request":request}).data
        return Response({"data":data,"meta":meta_data,"status":status.HTTP_200_OK},status=status.HTTP_200_OK)


class ViewPurchasedPlan(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["Subscriptions"],
        operation_id="view_purchased_plans_list",
        operation_description="View Purchased Plans List",
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_QUERY,description="Plan Id",type=openapi.TYPE_STRING),
        ],
    )
    def get(self, request, *args, **kwargs):
        try:
            plan=UserPlanPurchased.objects.get(id=request.query_params.get('id'))
        except:
            return Response({"message":"Purchased plan not found!","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        data = PurchasedPlanSerializer(plan,context = {"request":request}).data
        return Response({"data":data,"status":status.HTTP_200_OK},status=status.HTTP_200_OK)



class BuySubscriptionPlan(APIView):
    permission_classes=(permissions.IsAuthenticated,)
    parser_classes=[MultiPartParser]

    @swagger_auto_schema(
        tags=["Subscriptions"],
        operation_id="buy_subscription",
        operation_description="Buy Subscription",
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_FORM, type=openapi.TYPE_STRING,description=('Subscription Plan Id')),
        ],
    )
    def post(self,request,*args,**kwargs):
        try:
            user=User.objects.get(id=request.user.id,role_id=CUSTOMER)
        except:
            return Response({"message":"User does not exists!","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        try:
            plan=SubscriptionPlans.objects.get(id=request.data.get('id'))
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
        #generating invoice
        # target_name = f"subscription-invoice-{purchased_plan.plan_id}.pdf"
        # pdf = render_to_pdf_file(request,'pdf-templates/subscription_invoice.html',context={
        #                 'plan':purchased_plan
        #             })
        # purchased_plan.invoice.save(target_name, File(BytesIO(pdf.content)))

        activate_subscription(user)
        user.save()

        ## for managing transactions 
        # create_subscription_transaction(
        #     user = request.user,
        #     total_amount = purchased_plan.final_amount,
        #     purchase_plan=purchased_plan,
        #     transaction_for=PAYMENT_PLAN_PURCHASE
        # )
        ## send notification to admin
        # send_notification(
        #     created_by = user,
        #     created_for = None,
        #     title = f"User : {user.full_name.capitalize()} purchased subscription plan",
        #     description =  f"User :  {user.full_name.capitalize()} purchased subscription plan",
        #     notification_type = NOTIFICATION_SUBSCRIPTION,
        #     obj_id = str(purchased_plan.id),
        # )
        data = PurchasedPlanSerializer(purchased_plan,context = {"request":request}).data
        return Response({"message":"Plan purchased successfully!","data":data,"status":status.HTTP_200_OK},status=status.HTTP_200_OK)


class CurrentPLanInformation(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        tags=["Subscriptions"],
        operation_id="view_current_plan_information",
        operation_description="View Current Plan Information",
        manual_parameters=[
        ],
    )
    def get(self, request, *args, **kwargs):
        purchased_plan = UserPlanPurchased.objects.filter(purchased_by=request.user).order_by('created_on').last()
        data = PurchasedPlanSerializer(purchased_plan,context = {"request":request}).data
        return Response({"data":data,"status":status.HTTP_200_OK},status=status.HTTP_200_OK)


class PayAndRenewPlan(APIView):
    permission_classes=(permissions.IsAuthenticated,)
    parser_classes=[MultiPartParser]

    @swagger_auto_schema(
        tags=["Subscriptions"],
        operation_id="pay_renew_subscription_plan",
        operation_description="Pay & Renew Subscription Plan ( After subscription plan expire )",
        manual_parameters=[
            openapi.Parameter('payment_response', openapi.IN_FORM, type=openapi.TYPE_STRING,description=('Complete payment response')),
            openapi.Parameter('transaction_id', openapi.IN_FORM, type=openapi.TYPE_STRING,description=('Payment Transaction Id')),
        ],
    )
    def post(self,request,*args,**kwargs):
        try:
            user=User.objects.get(id=request.user.id,role_id=CUSTOMER)
        except:
            return Response({"message":"User does not exists!","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        
        ## validate plans
        if not user.is_plan_purchased:
            return Response({"message":"Invalid request","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        
        if user.is_subscription_active:
            return Response({"message":"Sorry , can not activate this plan at the moment as you already have active plan.","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
        
        first_purchased_plan=UserPlanPurchased.objects.filter(purchased_by=user).order_by('created_on').first()

        purchased_plan = first_purchased_plan.subscription_plan

        if purchased_plan.is_deleted == True or purchased_plan.status == False:
            return Response({"message":"Subscription plan does not exist!","status":status.HTTP_400_BAD_REQUEST},status=status.HTTP_400_BAD_REQUEST)
    
        first_purchased_plan.status = USER_PLAN_IN_QUEUE,
        first_purchased_plan.amount = purchased_plan.price,
        first_purchased_plan.final_amount = purchased_plan.final_price,
        first_purchased_plan.features = purchased_plan.features,
        first_purchased_plan.month_year = purchased_plan.month_year,
        first_purchased_plan.validity = purchased_plan.validity,
        first_purchased_plan.is_subscription_renewal = True
        
        #generating invoice
        target_name = f"subscription-invoice-{first_purchased_plan.plan_id}.pdf"
        pdf = render_to_pdf_file(request,'pdf-templates/subscription_invoice.html',context={
                        'plan':purchased_plan
                    })
        first_purchased_plan.invoice.save(target_name, File(BytesIO(pdf.content)))
        first_purchased_plan.save()
        
        activate_subscription(user)

        # ## for managing transactions 
        # create_subscription_transaction(
        #     user = request.user,
        #     total_amount = purchased_plan.final_amount,
        #     purchase_plan=purchased_plan,
        #     transaction_for=PAYMENT_PLAN_PURCHASE
        # )
        ## send notification to admin
        # send_notification(
        #     created_by = user,
        #     created_for = None,
        #     title = f"User : {user.full_name.capitalize()} purchased subscription plan",
        #     description =  f"User :  {user.full_name.capitalize()} purchased subscription plan",
        #     notification_type = NOTIFICATION_SUBSCRIPTION,
        #     obj_id = str(purchased_plan.id),
        # )
        data = PurchasedPlanSerializer(purchased_plan,context = {"request":request}).data
        return Response({"message":"Plan activated successfully!","data":data,"status":status.HTTP_200_OK},status=status.HTTP_200_OK)


