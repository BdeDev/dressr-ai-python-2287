import stripe
from accounts.utils import *
from accounts.models import *
from credentials.models import *

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



def generate_oxxo_reference(request,amount, user):
    set_stripe_keys()
    try:
        # Amount in cents (e.g., 1000 = 10.00 MXN)
        payment_intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),  # Stripe uses centavos
            currency="mxn",
            payment_method_types=["oxxo"],
            receipt_email=user.email,
            metadata={
                "user_id": str(user.id),
                "user_email": user.email,  # Helps track fraud patterns
                "user_ip": request.META.get("REMOTE_ADDR"),  # If available in your model
                "device_info": request.headers.get("User-Agent"),  # Helps Stripe Radar detect anomalies
            }
        )
        oxxo_display_details = payment_intent.next_action.oxxo_display_details
        return {
            "reference": oxxo_display_details.number,
            "expires_at": oxxo_display_details.expires_after,
            "barcode_url": oxxo_display_details.hosted_voucher_url,
            "payment_intent_id": payment_intent.id,
        }
    except Exception as e:
        db_logger.exception(e)
        return None
    


def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload=payload, sig_header=sig_header, secret=endpoint_secret
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    status = process_stripe_event(event)

    return HttpResponse(status=200), status


def process_stripe_event(event) -> str:
    """
    Process Stripe webhook event and handle wallet/transaction logic.
    Returns: 'success', 'failed', 'expired', or 'unknown'
    """
    event_type = event.get('type')
    intent = event['data']['object']

    if event_type == 'payment_intent.succeeded':
        try:
            metadata = intent.get('metadata', {})
            user_email = metadata.get('user_email')
            reference = intent['next_action']['oxxo_display_details']['number']
            expires_at = intent['next_action']['oxxo_display_details']['expires_after']
            amount_cents = intent.get('amount', 0)
            user  = User.objects.filter(email=user_email).first()
            user_wallet =  get_user_wallet(user)
            # Prevent duplicates
            if Transactions.objects.filter(transaction_id=intent['id']).exists():
                return 'success'

            # Create transaction
            transaction = Transactions.objects.create(
                unique_invoice_no=GenerateInvoiceNumber(),
                transaction_id=intent['id'],
                amount=amount_cents / 100, # Convert cents to actual amount
                payment_status=True,
                transaction_type=AMOUNT_RECIEVED,
                payment_type=TRANSFER_MONEY_FROM_WALLET,
                transaction_made_via=TRANSACTION_VIA_OXXO,
                created_by=user_email,
                oxxo_code=reference,
            )

            wallet_history = WalletHistory.objects.filter(wallet=user_wallet, oxxo_code=reference).first()
            if wallet_history:
                wallet_history.wallet_transaction_id = generate_wallet_transaction_id()
                wallet_history.transaction = transaction
                wallet_history.wallet_transaction_type = AMOUNT_RECIEVED
                wallet_history.save()

            oxxo_payment = OxxoPayment.objects.filter(created_by=user, barcode_url=intent['next_action']['oxxo_display_details']['hosted_voucher_url'], expires_at=expires_at).last()
            if oxxo_payment:
                oxxo_payment.is_paid = True
                oxxo_payment.save()
                
            # Manage wallet
            admin_wallet = get_user_wallet(None)  # None for system wallet
            WalletHistory.objects.create(
                wallet_transaction_id=generate_wallet_transaction_id(),
                wallet=admin_wallet,
                transaction=transaction,
                amount=transaction.amount,
                wallet_transaction_type=AMOUNT_PAID,
                payment_for=WALLET_TRANSFER_MONEY,
            )
            admin_wallet.balance -= transaction.amount
            admin_wallet.save()

            return 'success'

        except Exception as e:
            # Log error if needed
            db_logger.exception("Error processing Stripe success event: %s", str(e))
            return 'failed'

    elif event_type == 'payment_intent.payment_failed':
        return 'failed'

    elif event_type == 'payment_intent.canceled':
        return 'expired'

    return 'unknown'


def get_payment_from_oxxo(request, oxxo_reference):
    oxxo_reference = oxxo_reference.strip()
    try:
        set_stripe_keys()
        payment_intent = stripe.PaymentIntent.list(
            limit=100,
            status='succeeded',
            next_action='oxxo_display_details',
            metadata={'oxxo_reference': oxxo_reference}
        )
        intent = payment_intent['data']['objects']
        amount_cents = intent.get('amount', 0)

        # Create transaction
        transaction = Transactions.objects.create(
            unique_invoice_no=GenerateInvoiceNumber(),
            transaction_id=payment_intent['id'],
            amount=amount_cents / 100, # Convert cents to actual amount
            payment_status=True,
            transaction_type=AMOUNT_RECIEVED,
            payment_type=TRANSFER_MONEY_FROM_WALLET,
            transaction_made_via=TRANSACTION_VIA_OXXO,
            created_by=get_admin(),
            oxxo_code=oxxo_reference,
        )

        # admin wallet management
        wallet=get_user_wallet(None)
        wallet_history = WalletHistory.objects.create(
            oxxo_code=oxxo_reference,
            wallet_transaction_id=generate_wallet_transaction_id(),
            wallet=wallet,
            transaction=transaction,
            amount=transaction.amount,
            wallet_transaction_type=AMOUNT_RECIEVED,
            payment_for=WALLET_ADD_MONEY,

            )
    
        wallet.balance += transaction.amount
        wallet.save()
    except Exception as e:
        db_logger.exception(e)

