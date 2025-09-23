from django.db import models

# Create your models here.
from django.db import models
from accounts.models import *
from jsonfield import JSONField


class SubscriptionPlans(CommonInfo):
    title = models.CharField(max_length=255, null=True, blank=True)
    price = models.FloatField(null=True, blank=True) ## per month
    final_price = models.FloatField(null=True, blank=True) ## calculated based on permonth price * 12
    features = models.TextField(null=True, blank=True)
    month_year = models.IntegerField(null=True, blank=True,default=1)
    validity = models.PositiveIntegerField(default=MONTHLY_PLAN,null=True, blank=True, choices=PLAN_VALIDITY)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    # Feature limits
    max_uploads = models.PositiveIntegerField(default=50)      # e.g., number of wardrobe items
    max_try_ons = models.PositiveIntegerField(default=5)       # e.g., virtual try-ons
    max_shares = models.PositiveIntegerField(default=1)        # e.g., wardrobes shared

    class Meta:
        db_table = 'subscription_plans'


class UserPlanPurchased(CommonInfo):
    plan_id = models.CharField(max_length=100, null=True, blank=True)
    subscription_plan = models.ForeignKey(SubscriptionPlans, null=True, blank=True, on_delete=models.CASCADE)
    purchased_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    status = models.PositiveIntegerField(default=USER_PLAN_IN_QUEUE,null=True, blank=True, choices=USER_PLAN_STATUS)
    amount = models.FloatField(null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    features = models.TextField(null=True, blank=True)
    month_year = models.IntegerField(null=True, blank=True,default=1)
    validity = models.PositiveIntegerField(default=MONTHLY_PLAN,null=True, blank=True, choices=PLAN_VALIDITY)
    activated_on = models.DateTimeField(auto_now=False,null=True,blank=True)
    expire_on = models.DateTimeField(auto_now=False,null=True,blank=True)
    invoice = models.FileField(upload_to='subscription_invoices',null=True,blank=True)
    final_amount = models.FloatField(null=True, blank=True) ## calculated based on permonth price * 12
    is_subscription_renewal = models.BooleanField(default=False)
    renewable_count = models.IntegerField(default=0, null=True, blank=True,)
    marked_expired_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,related_name="marked_expired_by")

    
    class Meta:
        managed = True
        db_table = 'user_plan_purchased'
        default_permissions = ()

    
class Transactions(CommonInfo):
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)
    response = JSONField(null=True, blank=True)
    payment_status = models.BooleanField(default=False)
    purchased_plan = models.ForeignKey(UserPlanPurchased, null=True, blank=True, on_delete=models.CASCADE)
    transaction_for = models.PositiveIntegerField(choices = PAYMENT_PROCRESS_FOR, null=True, blank=True,default=PAYMENT_PLAN_PURCHASE)
    transaction_type = models.PositiveIntegerField(choices = TRANSACTION_TYPE, null=True, blank=True,default=AMOUNT_PAID)
    payment_type = models.PositiveIntegerField(choices = PAYMENT_TYPE, null=True, blank=True,default=PAYMENT_ONLINE)
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    

    class Meta:
        managed = True
        db_table = 'trasactions'
        default_permissions = ()


class UserWallet(CommonInfo):
    amount = models.FloatField(null=True, blank=True, default=0)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,default=None)
    total_earning = models.FloatField(null=True, blank=True, default=0)
    total_refunded = models.FloatField(null=True, blank=True, default=0)

    class Meta:
        managed = True
        default_permissions = ()
        db_table = 'wallet'


class UserWalletHistory(CommonInfo):
    wallet = models.ForeignKey(UserWallet,on_delete=models.CASCADE,null=True,blank=True)
    transaction = models.ForeignKey(Transactions,on_delete=models.CASCADE,null=True,blank=True)
    amount = models.FloatField(null=True, blank=True, default=0)
    action_type = models.PositiveIntegerField(default=WALLET_AMOUNT_CREATED, choices=WALLET_HISTORY_ACTION_TYPE,null=True, blank=True)
    purchased_plan = models.ForeignKey(UserPlanPurchased, null=True, blank=True, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
   

    class Meta:
        managed = True
        default_permissions = ()
        db_table = 'wallet_history'
