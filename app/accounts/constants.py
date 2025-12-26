USE_HTTPS = False
DEFAULT_TIMEZONE='Asia/Kolkata'
MAX_ACTIVE_BANNER = 5
SHOW_MORE_COUNT = 5
DEFAULT_SERVICE_FEES = 5
DEFAULT_CONVENIENCE_FEES = 5
MAX_PROVIDERS_KEY = 3

'''
Used in development mode
'''
RELEASE_DATE = "2026-04-20"

"""
User role type name
"""
USER_ROLE = ((1, "Admin"),(2, "Customer"),(3, "Affiliate"))
ADMIN = 1
CUSTOMER = 2
AFFILIATE = 3

"""
User Status 
"""
USER_STATUS = ((1, "Active"),(2,"Inactive"),(3,"Deleted"),(4,"Pause"))
ACTIVE = 1
INACTIVE = 2
DELETED = 3

"""
GENDER
"""
GENDER = ((1, 'Male'),(2,'Female'),(3,'Other'),(4,'Unisex'))
MALE = 1
FEMALE = 2
OTHER= 3
UNISEX= 4

"""
MARITAL_STATUS
"""
MARITAL_STATUS = ((1, 'MARRIED'),(2,'UNMARRIED'),(3,'WIDOW'),(4,'DIVORCED'))
MARRIED = 1
UNMARRIED = 2
WIDOW = 3
DIVORCED = 4 

"""
Device
"""
DEVICE_TYPE  = ((1,"Android"),(2,"IOS"))
ANDROID = 1
IOS = 2

"""
PAGE SIZE
"""
PAGE_SIZE = 20
API_PAGINATION = 10

'''
Notification Type
'''
NOTIFICATION_TYPE = ((1,'Admin Notification'),(2,'Loan Status Notification'),(3,'User Related Notification'),(3,'Query Ticket Notification'),(3,'Subscription Notification'))
ADMIN_NOTIFICATION=1
LOAN_STATUS_NOTIFICATION = 2
USER_RELATED_NOTIFICATION = 3
QUERY_TICKET_NOTIFICATION = 4
SUBSCRIPTION_STATUS_NOTIFICATION = 5

"""
LOGIN_STATE
"""
LOGIN_STATE = ((1,'Login Success'),(2,'Login Failure'))
LOGIN_SUCCESS = 1
LOGIN_FAILURE = 2

"""
Page Type
"""
PAGE_TYPE =  ((1,"Terms_And_Condition"),(2,"Privacy_Policy"),(3, "About_Us"),(4, "How_it_works"),(6, "contact_us"), (7, "Pricing"))
TERMS_AND_CONDITION = 1
PRIVACY_POLICY = 2
ABOUT_US = 3
HOW_IT_WORKS = 4
# COOKIE_POLICY = 5
CONTACT_US = 6
PRICING = 7

"""
SOCIAL TYPE
"""
SOCIAL_TYPE = ((1, 'Google'), (2, 'Facebook'), (3, 'Apple'), (4, 'X'), (5, 'Linkedin'),(6,'Others'))
GOOGLE = 1
FACEBOOK = 2
APPLE = 3
X = 4
LINKEDIN = 5
OTHERS = 6


'''
EMAIL STATUS
'''
EMAIL_STATUS = ((1,'EMAIL_SENT'),(2,'EMAIL_PENDING'),(3,'EMAIL_FAILED'))
EMAIL_SENT = 1
EMAIL_PENDING = 2
EMAIL_FAILED = 3


STYLE = [(1, "Casual"),(2, "Formal"),(3, "Party"),(4, "Street Style"),(5, "Classic")]
CASUAL = 1
FORMAL = 2
PARTY = 3
STREET_STYLE = 4
CLASSIC = 5

WEATHER_TYPE = [(1, "Summer"),(2, "Winter"),(3, "Rainy"),(4, "Spring"),(5, "All Seasons")]
SUMMER = 1
WINTER = 2
RAINY = 3
SPRING  = 4
ALL_SEASONS = 5

PLAN_VALIDITY = [(1,'Monthly'),(2,'Yearly')]
MONTHLY_PLAN = 1
YEARLY_PLAN = 2

"""
Subscription Plan Satus
"""
PLAN_STATUS = [(1,'PLAN_ACTIVE'),(2,'PLAN_INACTIVE')]
PLAN_ACTIVE = 1
PLAN_INACTIVE = 2

"""
User subscription Plan Status
"""
USER_PLAN_STATUS = ((1,'PLAN_ACTUSER_PLAN_ACTIVEIVE'),(2,'PLANUSER_PLAN_IN_QUEUE_IN_QUEUE'),(3,'USER_PLAN_EXPIRED'),(4,'USER_PLAN_CANCELLED'))
USER_PLAN_ACTIVE = 1
USER_PLAN_IN_QUEUE = 2
USER_PLAN_EXPIRED = 3
USER_PLAN_CANCELLED = 4

"""
PAYMENT_PROCRESS_FOR
"""
PAYMENT_PROCRESS_FOR = ((1,'PAYMENT_PLAN_PURCHASE'),(2,'PAYMENT_NFT_CIRTIFICATE'))
PAYMENT_PLAN_PURCHASE = 1
PAYMENT_NFT_CIRTIFICATE = 2

"""
Wallet history 
"""
WALLET_HISTORY_ACTION_TYPE = ((1,'WALLET_AMOUNT_DEBITED'),(2,'WALLET_AMOUNT_CREATED'))
WALLET_AMOUNT_DEBITED = 1
WALLET_AMOUNT_CREATED = 2

"""
TRANSACTION_TYPE
"""
TRANSACTION_TYPE = ((1,'Amount Paid'),(2,'Amount Refunded'))
AMOUNT_PAID = 1
AMOUNT_REFUNDED = 2


"""
PAYMENT_TYPE
"""
PAYMENT_TYPE = ((1,'PAYMENT_ONLINE'),(2,'PAYMENT_CASH'))
PAYMENT_ONLINE = 1
PAYMENT_CASH = 2

PACKING_CATEGORY = [(1, "Clothing"),(2, "Footwear"),(3, "Accessory"),(4, "Gear"),]
CLOTHING = 1
FOOTWEAR = 2
ACCESSORY = 3
GEAR = 4

SOURCE_CHOICES = [(1,'Wardrobe'),(1,'Recommended')]
WARDROBE = 1
RECOMMENDED = 2


#Affiliate Constants
COMMISSION_TYPE=((1, "Percentage of sale"),)
PERCENTAGE_OF_SALE=1


COMMISSION_HISTORY_STATUS=((1, "Pending"),(2, "Approved"),(3, "Paid"))
COMMISSION_STATUS_PENDING=1
COMMISSION_STATUS_APPROVED=2
COMMISSION_STATUS_PAID=3


TRY_ON_STATUS = ((1, "Pending"),(2, "Processing"),(3, "Success"),(4, "Failed"))
TRY_ON_PENDING = 1
TRY_ON_PROCESSING = 2
TRY_ON_SUCCESS = 3
TRY_ON_FAILED = 4


SIGMENT_TYPE = ((0,"Upper Body"),(1,"Lower Body"),(2,"Full Body"),(3,"Shoes"),(4,"Sunglasses"))
UPPER_BODY = 0
LOWER_BODY = 1
FULL_BODY = 2
SHOES = 3
SUNGLASSES = 4

INTEGRATION_TYPE = ((1,"API"),(2,"FEED"),(3,"MANUAL"))
API = 1
FEED = 2
MANUAL = 3


CLOTH_CATEGORY_TYPE = ((1,"Top"),(2,"Bottom"),(3,"Dress"),(4,"Jacket"),(5,"Shoes"),(6,"Goggles"),(7,"Purse"),(8,"Hat"))
TOP = 1
BOTTOM = 2
DRESS = 3
JACKET = 4
SHOES_CAT = 5
GOGGLES = 6
PURSE = 7
HAT = 8