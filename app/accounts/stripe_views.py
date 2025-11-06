import stripe
from accounts.utils import *
from accounts.models import *
from credentials.models import *
import time
from django.views.decorators.csrf import csrf_exempt

def GetStripeKeys():
    stripe_keys = StripeSetting.objects.filter(active=True).first()
    if not stripe_keys:
        stripe_keys,created = StripeSetting.objects.get_or_create(test_publishkey=env('STRIPE_PUBLISH_KEY'),test_secretkey=env('STRIPE_SECRET_KEY'))
        stripe_keys.active=True
        stripe_keys.save()
    test_publishkey=stripe_keys.test_publishkey
    test_secretkey=stripe_keys.test_secretkey
    return test_publishkey,test_secretkey

def set_stripe_keys():
    GetStripeKeys()
    stripe.api_key = GetStripeKeys()[1] if GetStripeKeys()[1] else None
    return None

def CreateStripeCustomer(request:HttpRequest,user:User):
    is_created = False
    try:
        set_stripe_keys()
        if not user.is_superuser and not user.customer_id :
            stripe_customer = stripe.Customer.create(
                description = "Dressr-AI. - %s " % user.email,
                email = user.email,
                name = user.email,
            )
            user.customer_id = stripe_customer.id
            user.save()
            is_created = True
    except Exception as e:
        db_logger.exception(e)
    return is_created
    
def CreateStripeCard(user:User,card_token:str):
    try:
        set_stripe_keys()
        card=stripe.Customer.create_source(
            user.customer_id,
            source = card_token,
        )
        return card
    except Exception as e:
        db_logger.exception(e)
        return False

def CheckDuplicateCard(user:User,card_token:str):
    is_duplicate = True
    duplicate_card=None
    try:
        set_stripe_keys()
        existing_cards = stripe.Customer.list_sources(user.customer_id,object="card")
        duplicate_card = next((card for card in existing_cards if card.fingerprint == stripe.Token.retrieve(card_token).card.fingerprint),None)
        if not duplicate_card:
            is_duplicate =  False
    except Exception as e:
        db_logger.exception(e)
    return is_duplicate,duplicate_card

def StripeAllCards(user:User):
    try:
        set_stripe_keys()
        cards = stripe.Customer.list_sources(user.customer_id,object="card")
        cards_list = []
        for card in cards['data']:
            data = {'name':card['name'],'card_id':card['id'],'exp_month':card['exp_month'],'exp_year':str(card['exp_year']),'card_holder_name':card['name'],'last4':card['last4'],'brand':card['brand']}
            cards_list.append(data)
        return cards_list
    except Exception as e:
        db_logger.exception(e)
        return []
    
def DeleteStripeCard(user:User,card_id:str):
    try:
        set_stripe_keys()
        stripe.Customer.delete_source(
            user.customer_id,
            card_id
        )
        return True
    except Exception as e:
        db_logger.exception(e)
        return False

def CreateStripeBankAccount(user:User,account_holder_name:str,routing_number,account_number):
    try:
        set_stripe_keys()
        stripe_bank_account = stripe.Token.create(
            bank_account={
                "country": 'US',  ## country code in Capital
                "currency": 'EUR',
                "account_holder_name": account_holder_name,
                "routing_number": routing_number,
                "account_number": account_number,
            }
          )
        stripe.Customer.create_source(
            user.customer_id,
            source = stripe_bank_account.id,
        )
        
        return True
    except Exception as e:
        db_logger.exception(e)
        return False

def StripeBankAccountDetails(user:User):
    try:
        set_stripe_keys()
        bank_account = stripe.Customer.list_sources(user.customer_id,object="bank_account")
        return bank_account['data'][0]
    except Exception as e:
        db_logger.exception(e)
        return []
    
def DeleteStripeBankAccount(user:User,bank_id):
    try:
        set_stripe_keys()
        stripe.Customer.delete_source(user.customer_id,bank_id)
        return True
    except Exception as e:
        db_logger.exception(e)
        return False
    
def CreateStripeTransaction(request,user:User,amount,description,card_id):
    try:
        set_stripe_keys()
        payment_intent=stripe.PaymentIntent.create(
            amount=int(float(amount)*100),
            currency="USD",
            payment_method_types=["card"],
            customer = user.customer_id,
            description = description,
            confirm=True,
            payment_method=card_id,
            off_session=True,
            metadata={
                "user_id": str(user.id),
                "user_email": user.email,  # Helps track fraud patterns
                "transaction_description": description,
                "user_ip": request.META.get("REMOTE_ADDR"),  # If available in your model
                "device_info": request.headers.get("User-Agent"),  # Helps Stripe Radar detect anomalies
            }
        )
        captured_reciept_url = stripe.Charge.retrieve(
            payment_intent.latest_charge,
        )
        if not captured_reciept_url.paid:
            return None
        return captured_reciept_url
    except Exception as e:
        db_logger.exception(e)
        return None

def create_connected_account(user):
    """
    Create a Connected Account for a loan recipient
    
    Parameters:
        user_email (str): The email of the recipient
        user_name (str): The full name of the recipient
    
    Returns:
        str: The ID of the created account
    """
    try:    
        if not user.account_id:
            set_stripe_keys()
            account = stripe.Account.create(
                type="custom",
                country="MX",
                email=user.email,
                business_type="individual",
                individual={
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "dob": {
                        "day": 1,
                        "month": 1,
                        "year": 1980
                    },
                    "address": {
                        "city": "Mexico City",
                        "state": "Jalisco",
                        "country": "MX",
                        "line1": "123 Main Street",
                        "postal_code": "11560"
                    },
                    "phone": "+5215555555555",
                    "email": user.email,
                    "id_number": "ABCD123456XYZ",
                    "political_exposure": "none"
                },
                business_profile={
                    "url": "https://barobarato.com",
                    "mcc": "6012"
                },
                tos_acceptance={
                    "date": int(time.time()),
                    "ip": "127.0.0.1"
                },
                capabilities={
                    "transfers": {"requested": True}, 
                    "card_payments": {"requested": True},  
                    "mx_bank_transfer_payments": {"requested": True},
                },
                settings={"payouts": {"schedule": {"interval": "manual"}}}, ## to manage payout manually
            )
            user.account_id = account.id
            user.save()
            print(f"New Account Created: {account.id}")
            return account.id
        else:
            return user.account_id  
    except Exception as e:
        print(f"Error creating new account: {e}")
        db_logger.exception(e)
        return None
    
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        return HttpResponse(status=400)  # Invalid payload
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)  # Invalid signature

    if event['type'] == 'invoice.payment_succeeded':
        # Subscription renewed
        data = event['data']['object']
        customer_id = data['customer']
        print(f"✅ Subscription renewed for customer {customer_id}")

    return HttpResponse(status=200)
